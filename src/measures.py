"""The five governance measures M1 to M5.

Phase 5. Every measure returns findings carrying a non-empty caveat, which test
T10 checks. Every number published by the site comes from here (S5).

Rules applied, from governance/decision-rules.md:
- M1  one row is one use case. Candidates flagged, never merged. All three
      similarity thresholds published together. The consolidated route is shown
      beside the headline and never summed with it.
- M2  completeness is reported within one year only. The 2024 inventory is a
      schema reference and its rows are not read.
- M3  freshness is a finding, not a metric. Triggers are a diagnostic reported
      in two groups.
- M4  the subset is the 445 labelled high-impact. Two further bands are labelled
      separately and the full arithmetic is shown.
- M5  fields asked, never volume.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW = REPO_ROOT / "data" / "raw"
DERIVED = REPO_ROOT / "data" / "derived"

SIMILARITY_THRESHOLDS = (0.95, 0.85, 0.70)

NEVER_SUM = (
    "The headline count of 3,611 includes nothing from the second route. The two count "
    "different things: one counts systems, the other counts an agency ticking a task on a "
    "shared list. Adding them would produce a number that means nothing."
)
FILLED_FIELD = (
    "A filled field shows that information was provided, not that the practice is adequate. "
    "An empty field is not evidence that the practice is absent."
)


def _empty_rule() -> tuple[set[str], set[str], dict[str, str]]:
    rule = json.loads((RAW / "empty_value_rule.json").read_text())
    dic = json.loads((RAW / "omb2025_data_dictionary.json").read_text())
    types = {k: (v.get("data_type") or "free_text") for k, v in dic.items()}
    return set(rule["empty_always"]), set(rule["empty_in_text_and_url_fields_only"]), types


def is_empty(column: str, value, always: set[str], text_only: set[str], types: dict[str, str]) -> bool:
    """A value records an absence. Field type decides, per decision-rules section 13."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return True
    s = str(value).strip().lower()
    if s in always:
        return True
    return types.get(column, "free_text") in {"free_text", "date", "url"} and s in text_only


def completeness(df: pd.DataFrame) -> dict[str, float]:
    always, text_only, types = _empty_rule()
    out = {}
    for c in df.columns:
        filled = (~df[c].map(lambda v: is_empty(c, v, always, text_only, types))).mean()
        out[c] = round(float(filled) * 100, 1)
    return out


def _key(s) -> str:
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", str(s).lower()).split())


def m1_unit_of_registration(reg: pd.DataFrame, cots: pd.DataFrame) -> dict:
    """What counts as one use case. Candidates flagged, never merged."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    text = (reg["use_case_name"].fillna("") + " " + reg["problem_solved"].fillna("")).map(_key)
    X = TfidfVectorizer(min_df=2, stop_words="english", ngram_range=(1, 2),
                        max_features=60000).fit_transform(text)

    bands = []
    flagged_at_top = set()
    for thr in SIMILARITY_THRESHOLDS:
        rows, pairs = set(), 0
        for a in range(0, X.shape[0], 500):
            blk = cosine_similarity(X[a:a + 500], X)
            for i in range(blk.shape[0]):
                gi = a + i
                for j in np.where(blk[i] >= thr)[0]:
                    if j > gi:
                        pairs += 1
                        rows.add(gi)
                        rows.add(int(j))
        bands.append({"threshold": thr, "candidate_pairs": pairs,
                      "entries_flagged": len(rows),
                      "share_of_register": round(len(rows) / len(reg) * 100, 1)})
        if thr == SIMILARITY_THRESHOLDS[0]:
            flagged_at_top = set(rows)

    k = reg["use_case_name"].map(_key)
    within = reg.groupby([reg["agency_name"], k]).size()
    across = reg.groupby(k)["agency_name"].nunique()

    return {
        "measure": "M1",
        "question": "Is the same AI capability registered once, many times, or folded into something else?",
        "rule_applied": "One row is one use case. Candidates are flagged and never merged, and no total is adjusted.",
        "individually_reported_entries": int(len(reg)),
        "consolidated_route": {
            "rows": int(len(cots)),
            "agencies": int(cots["Agency"].nunique()),
            "distinct_common_tasks": int(cots["AI Use Case"].nunique()),
            "agency_task_combinations_in_use": int((cots["Agency Use (Y/N)?"] == "Y").sum()),
        },
        "never_summed_reason": NEVER_SUM,
        "candidate_duplicates_not_confirmed": bands,
        "exact_name_repeats_within_one_agency": {
            "names": int((within > 1).sum()), "rows": int(within[within > 1].sum())},
        "same_name_used_by_more_than_one_agency": int((across > 1).sum()),
        "entries_flagged_at_highest_threshold": sorted(int(i) for i in flagged_at_top),
        "caveat": (
            "Comparing wording cannot show that two entries are the same system. Entries that read "
            "alike may be one system written down twice, or two different systems described in "
            "similar words. The count triples depending on how alike they have to be, so it is a "
            "choice about where to draw a line rather than something the file contains. All three "
            "settings are shown for that reason. Nothing has been merged and no total changed."
        ),
    }


CORE_FIELDS = ["id", "use_case_name", "agency_bureau", "development_stage", "is_high_impact",
               "topic_area", "classification", "problem_solved", "benefits", "system_outputs",
               "operational_date", "contracting_usage", "have_ato", "data_description",
               "has_pii", "demographic_features", "has_custom_code"]


def completeness_per_entry(reg: pd.DataFrame) -> pd.Series:
    """How many core fields hold a value, counted separately for each entry.

    This is a per-entry count. It is not an agency average, and no agency-level
    figure is derived from it.
    """
    always, text_only, types = _empty_rule()
    return sum((~reg[c].map(lambda v: is_empty(c, v, always, text_only, types))).astype(int)
               for c in CORE_FIELDS)


def m2_completeness_shape(reg: pd.DataFrame) -> dict:
    """Whether per-entry completeness varies inside a submission.

    Reported because the same whole-submission shape appears in the oversight
    block: values arrive together rather than entry by entry.
    """
    import statistics

    per_entry = completeness_per_entry(reg)
    frame = pd.DataFrame({"agency": reg["agency_name"], "n": per_entry})
    distinct, concentration, single = {}, {}, []
    for agency, group in frame.groupby("agency"):
        counts = group["n"].value_counts()
        distinct[agency] = int(counts.size)
        concentration[agency] = float(counts.iloc[0] / len(group))
        if counts.size == 1:
            single.append(agency)
    rows_in_single = int(frame["agency"].isin(single).sum())
    dominant = [a for a, s in concentration.items() if s > 0.8]
    return {
        "core_fields_counted": len(CORE_FIELDS),
        "distinct_values_across_the_register": int(per_entry.nunique()),
        "possible_values": len(CORE_FIELDS) + 1,
        "median_distinct_values_within_one_agency": int(statistics.median(distinct.values())),
        "agencies_where_every_entry_shares_one_value": len(single),
        "entries_in_those_agencies": rows_in_single,
        "agencies_where_over_four_fifths_share_one_value": len(dominant),
        "entries_in_those_agencies_too": int(frame["agency"].isin(dominant).sum()),
        "median_share_of_entries_at_an_agency_most_common_value": round(
            statistics.median(concentration.values()) * 100, 1),
        "statement": (
            "An entry can hold anywhere from none of these fields to all seventeen. Almost every "
            "one of those levels occurs somewhere in the list. Inside a single agency, almost "
            "every entry sits at the same one or two levels."
        ),
        "caveat": (
            "This counts each entry on its own. No agency average is taken and no agency is "
            "compared with another. The pattern describes how information arrives in the file, in "
            "the same way the nine oversight fields do, and says nothing about how any agency "
            "works."
        ),
    }


def m2_preparation(reg: pd.DataFrame) -> dict:
    """How the published data was prepared before it was published.

    The dictionary carries a map from what agencies wrote to the categories the
    file publishes. Reading it shows how much variation was folded together, and
    that one published value is not in the map at all.
    """
    dictionary = json.loads((RAW / "omb2025_data_dictionary.json").read_text())
    mapping = dictionary["classification"].get("recoding_map") or {}
    folded = {
        name.split(":")[0]: {"written_forms_folded_in": len(forms), "forms": forms}
        for name, forms in mapping.items()
    }
    documented = {form for forms in mapping.values() for form in forms}
    present = set(reg["classification"].dropna().unique())
    undocumented = sorted(present - documented)
    return {
        "measure": "M2-preparation",
        "question": "What was done to this data before it was published?",
        "rule_applied": "Read from the publisher's own dictionary. Nothing here is inferred.",
        "categories_published": len(mapping),
        "written_forms_folded_into_them": sum(len(f) for f in mapping.values()),
        "per_category": folded,
        "one_form_named_two_categories": "Generative AI; Natural Language Processing (NLP)",
        "values_present_but_not_in_the_map": undocumented,
        "entries_carrying_them": int(reg["classification"].isin(undocumented).sum()),
        "caveat": (
            "Folding written variants into shared categories is ordinary preparation and is not a "
            "criticism of it. It is recorded because the categories a reader counts are the "
            "publisher's, not the agencies', and because one published value does not appear in "
            "the map that describes them."
        ),
    }


def m2_completeness(reg: pd.DataFrame) -> dict:
    """What the register holds and what is blank. Within one year only."""
    hi = reg[reg["is_high_impact"] == "High-impact"]
    return {
        "measure": "M2",
        "question": "Does the register hold everything it should, and is each entry filled in?",
        "rule_applied": "Completeness is reported within one year only. The earlier inventory is a schema reference and its rows are not read.",
        "rows": int(len(reg)),
        "field_completeness_all_rows": completeness(reg),
        "field_completeness_high_impact": completeness(hi),
        "completeness_shape": m2_completeness_shape(reg),
        "reconciliation": {
            "figures_that_match": {"individually reported use cases": 3611,
                                    "high-impact use cases": 445,
                                    "agencies reporting individually": 41,
                                    "agencies affirmatively reporting no AI": 2},
            "figures_that_do_not_match": {
                "deployed and piloted": {"published": 1818, "observed": 1480,
                                          "note": "The difference of 338 equals exactly the number of rows with no development stage recorded."},
                "total agency submissions": {"published": 56, "observed": 54},
                "agencies reporting consolidated off-the-shelf": {
                    "published": 46, "observed": 45,
                    "note": "The source's own per-agency table and the data file agree at 45. Only the summary bullet differs."},
            },
            "internal_disagreement_in_source_table": {
                "column": "deployed and piloted", "sum_of_rows": 1819, "stated_total": 1818, "difference": 1},
        },
        "caveat": (
            "These figures cannot be compared with the earlier year, because the two years ask "
            "different questions: a box left empty in one year may not exist at all in the other. "
            "A published list can only show what was declared, so nothing here says anything about "
            "systems nobody wrote down. Two fields store an empty answer as a pair of brackets that "
            "a spreadsheet counts as an answer, and every figure here treats them as empty. "
            + FILLED_FIELD
        ),
    }


def m3_freshness(reg: pd.DataFrame) -> dict:
    """How old the information is. A finding, not a metric."""
    always, text_only, types = _empty_rule()
    stage = reg["development_stage"]
    no_stage = int(stage.map(lambda v: is_empty("development_stage", v, always, text_only, types)).sum())
    od = reg["operational_date"].dropna().astype(str).str.strip()
    od = od[~od.str.lower().isin(always)]
    parsed = pd.to_datetime(od, errors="coerce", format="mixed")
    return {
        "measure": "M3",
        "question": "How old is the information in each entry, and what would trigger a re-check?",
        "rule_applied": "Freshness cannot be calculated from this data. The finding replaces the metric.",
        "finding": (
            "The register cannot express how current any entry is. It records no verification date, "
            "no update date and no review date. Its single date field records when a system became "
            "operational, which answers a different question."
        ),
        "date_fields_in_the_field_set": 1,
        "operational_date": {
            "rows_with_a_value": int(len(od)),
            "share_of_rows": round(len(od) / len(reg) * 100, 1),
            "values_that_parse": int(parsed.notna().sum()),
            "parse_rate": round(float(parsed.notna().mean()) * 100, 1),
            "values_that_cannot_be_resolved": int(parsed.isna().sum()),
            "usable_dates_as_share_of_all_rows": round(int(parsed.notna().sum()) / len(reg) * 100, 1),
            "values_dated_after_the_download_date": int((parsed > pd.Timestamp("2026-09-23")).sum()),
        },
        "development_stage_filter": {
            "rows_carrying_a_stage": int(len(reg) - no_stage),
            "rows_with_no_stage_recorded": no_stage,
            "coverage": round((len(reg) - no_stage) / len(reg) * 100, 1),
            "label": "Stage is not recency. A stage describes where a system is in its life, not when this entry was last checked.",
        },
        "re_verification_trigger_diagnostic": {
            "group_one": {
                "statement": "Fields touching each of these exist. None records a change, a date of change, or a prior value.",
                "triggers": ["owner of the system", "model or version", "data sources", "scope of use"],
            },
            "group_two": {
                "statement": "The degree of autonomy with which a system acts is not present in the 2025 field set. No field touches it at all.",
                "triggers": ["degree of autonomy"],
            },
            "why_reported_separately": (
                "No field records a change and no field exists are different statements. Reporting them "
                "together would understate the second."
            ),
        },
        "caveat": (
            "The one date says when a system started running, not when anyone last looked at its "
            "entry. A system running for years might have had its description checked last week or "
            "never, and nothing here can tell those apart. Dates written in a form that could mean "
            "two different days are not counted, because choosing one reading would invent a "
            "precision the file does not have."
        ),
    }


def m4_oversight_pack(reg: pd.DataFrame) -> dict:
    """What the register could hand over for its high-impact entries."""
    always, text_only, types = _empty_rule()
    bands = {
        "High-impact": int((reg["is_high_impact"] == "High-impact").sum()),
        "Not High-impact": int((reg["is_high_impact"] == "Not High-impact").sum()),
        "Presumed High-Impact, but Not High-impact": int(
            (reg["is_high_impact"] == "Presumed High-Impact, but Not High-impact").sum()),
        "classification not recorded": int(reg["is_high_impact"].isna().sum()),
    }
    hi = reg[reg["is_high_impact"] == "High-impact"]
    presumed = reg[reg["is_high_impact"] == "Presumed High-Impact, but Not High-impact"]
    hifields = [c for c in reg.columns if c.startswith("hi_")]
    answered = sum((~hi[c].map(lambda v: is_empty(c, v, always, text_only, types))).astype(int) for c in hifields)
    jf = (~presumed["HI_justification"].map(
        lambda v: is_empty("HI_justification", v, always, text_only, types))).mean()
    return {
        "measure": "M4",
        "question": "For every high-impact use case, can the register answer the questions an oversight body would ask?",
        "rule_applied": "The subset is the entries labelled high-impact only. Two further bands are labelled separately, using the data's own label.",
        "bands": bands,
        "bands_total": sum(bands.values()),
        "register_rows": int(len(reg)),
        "arithmetic_closes": sum(bands.values()) == len(reg),
        "subset_size": int(len(hi)),
        "oversight_field_coverage": {c: round(float((~hi[c].map(
            lambda v: is_empty(c, v, always, text_only, types))).mean()) * 100, 1) for c in hifields},
        "oversight_block_shape": {
            "all_nine_answered": int((answered == len(hifields)).sum()),
            "none_answered": int((answered == 0).sum()),
            "partially_answered": int(((answered > 0) & (answered < len(hifields))).sum()),
            "statement": "The nine oversight fields are answered together or not at all.",
        },
        "withholding_status": {
            "high_impact_entries": int(len(hi)),
            "high_impact_with_no_status": int(hi["is_withheld"].isna().sum()),
            "high_impact_share_blank": round(float(hi["is_withheld"].isna().mean()) * 100, 1),
            "all_entries": int(len(reg)),
            "all_entries_with_no_status": int(reg["is_withheld"].isna().sum()),
            "all_entries_share_blank": round(float(reg["is_withheld"].isna().mean()) * 100, 1),
            "field_is_required": True,
            "dictionary_question": "Should this AI use case be withheld from public reporting?",
            "caveat": (
                "A blank in a field asking whether something should be withheld is not evidence "
                "that anything was withheld. The field is required, so a blank here is different "
                "from a blank in a field that did not apply."
            ),
        },
        "presumed_band": {
            "rows": int(len(presumed)),
            "justification_fill_rate": round(float(jf) * 100, 1),
            "dictionary_note": (
                "The justification field is specified to appear only when this band is selected, so a low "
                "rate in the high-impact band is the specification working."
            ),
        },
        "caveat": (
            FILLED_FIELD + " The pattern describes what reached the file, not the oversight practice "
            "itself. This is a practice exercise modelled on a realistic request. It is not a response "
            "to a request from any body."
        ),
    }


def m5_design_comparison(reg_columns: list[str], ontario: pd.DataFrame) -> dict:
    """How two real registers differ in what they ask. Fields, never volume."""
    return {
        "measure": "M5",
        "question": "How do two real registers differ in what they ask, and what does that reveal about design choices?",
        "rule_applied": "Fields asked are compared, never volume. One table, inside the gaps view.",
        "federal_register": {"fields_published": len(reg_columns), "entries": 3611},
        "ontario_register": {"fields_published": int(len(ontario.columns)), "entries": int(len(ontario))},
        "asked_by_ontario_not_by_the_federal_register": [
            {"field": "Autonomous", "note": "Whether the system acts autonomously. Not present in the 2025 federal field set."},
            {"field": "Human in the loop", "note": "Whether a person is involved in the decision. Not present in the 2025 federal field set."},
            {"field": "User base", "note": "Who the system serves."},
        ],
        "asked_by_the_federal_register_not_by_ontario": [
            {"field": "unique identifier", "note": "Ontario publishes no identifier for an entry."},
            {"field": "high-impact classification and its justification", "note": "Ontario publishes no risk classification."},
            {"field": "nine oversight questions", "note": "Testing, impact assessment, independent review, monitoring, training, fail-safe, appeal, consultation, potential impacts."},
            {"field": "whether the entry is withheld from public reporting", "note": "No Ontario equivalent."},
        ],
        "naming_practice": (
            "The Ontario register names no vendor in its published fields. The federal register publishes "
            "a vendor name field, which is the field this project removes under its own safeguard."
        ),
        "caveat": (
            "The Ontario register holds three entries. This comparison is of what each register asks, "
            "never of how much either contains, and nothing here depends on the size of either."
        ),
    }
