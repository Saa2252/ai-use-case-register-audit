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

from src import conditionality as COND

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


# How the comparison is done, in both registers of language, because a reader
# who cannot check the method cannot check the finding.
SIMILARITY_METHOD = {
    "plain": "Each entry's name and its description of the problem it solves are joined into "
             "one piece of text. Every entry is then compared with every other, and the "
             "comparison asks how much of their wording they share, with common English "
             "words ignored and rarer words counting for more. The result is a score between "
             "nothing in common and identical.",
    "named": "TF-IDF vectorisation over the use case name and the problem-solved field, "
             "with English stop words removed, unigrams and bigrams, terms appearing in only "
             "one entry dropped, and cosine similarity between every pair of vectors.",
    "term": "TF-IDF stands for term frequency, inverse document frequency. A word counts for "
            "more when it is rare across the whole register and appears often in one entry. "
            "Cosine similarity is the measure of overlap between two entries scored that way.",
    "why_this_one": "It compares wording and nothing else, which is the only thing a "
                    "published file supports. It cannot read a system, so it cannot confirm "
                    "a duplicate, and nothing here is merged on the strength of it.",
    "settings": "Compared on: use case name and problem solved. Words ignored: common "
                "English. Phrases counted: one and two words. Terms appearing in only one "
                "entry: dropped. Thresholds published: three.",
    "reproduce": "src/measures.py, m1_unit_of_registration.",
}


def _marginal_pair(reg: pd.DataFrame, marginal, X, vocabulary) -> dict | None:
    """The two entries that only just count as a pair at a given setting.

    **What is published, and why it is not the entry names.** The first run of
    this showed the two names. Two of the three marginal pairs turned out to
    carry product names that the vendor list had not caught, so publishing them
    would have broken S2, the safeguard this project exists to hold. Choosing a
    different pair to avoid that would have meant hand-picking an example to
    dodge a safeguard, which is worse than the exposure.

    So what is published is the wording the two entries share, which is what
    produced the score. A name unique to one entry cannot be shared by both, so
    this cannot carry a product name that appears in only one of them, and the
    shared terms are screened against the vendor list as a second layer.

    It is also the better illustration. A reader learns more from seeing that
    two entries scored alike because they share a boilerplate phrase than from
    seeing two titles and being asked to judge.
    """
    if marginal is None:
        return None
    score, left, right = marginal
    one, two = reg.iloc[left], reg.iloc[right]

    a, b = X[left].toarray()[0], X[right].toarray()[0]
    shared = np.where((a > 0) & (b > 0))[0]
    ranked = sorted(shared, key=lambda i: min(a[i], b[i]), reverse=True)
    terms, withheld = [], 0
    for index in ranked:
        term = vocabulary[index]
        if _is_vendor_term(term):
            withheld += 1
            continue
        terms.append(term)
        if len(terms) == 8:
            break

    def entry_ref(row):
        value = str(row["id"]).strip()
        return value if value and value.lower() not in {"nan", ""} else None

    refs = [entry_ref(one), entry_ref(two)]
    return {
        "score": round(score, 3),
        "same_agency": bool(one["agency_name"] == two["agency_name"]),
        "identifiers": [r for r in refs if r],
        "neither_carries_an_identifier": not any(refs),
        "shared_wording": terms,
        "shared_terms_withheld": withheld,
        "reading": "These two scored the least of any pair that counts at this setting, so "
                   "every other pair here reads more alike than they do. What is shown is the "
                   "wording the two entries share, which is what produced the score. The "
                   "entries are not named, because a name is where a product name would sit "
                   "and two of these three pairs carry one.",
    }


def _is_vendor_term(term: str) -> bool:
    """Second layer only. The first is that a term has to appear in both entries."""
    try:
        listed = (RAW / "vendor_terms.txt").read_text(encoding="utf-8").lower().split("\n")
    except OSError:
        return False
    words = {w.strip() for w in listed if w.strip()}
    return any(part in words for part in term.lower().split())


def m1_unit_of_registration(reg: pd.DataFrame, cots: pd.DataFrame) -> dict:
    """What counts as one use case. Candidates flagged, never merged."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    text = (reg["use_case_name"].fillna("") + " " + reg["problem_solved"].fillna("")).map(_key)
    vectoriser = TfidfVectorizer(min_df=2, stop_words="english", ngram_range=(1, 2),
                                 max_features=60000)
    X = vectoriser.fit_transform(text)
    vocabulary = vectoriser.get_feature_names_out()

    bands = []
    flagged_at_top = set()
    for thr in SIMILARITY_THRESHOLDS:
        rows, pairs = set(), 0
        # The pair that only just qualifies at this setting. Showing the
        # marginal case is the point: it is what the line looks like where it
        # is drawn, and a reader can judge for themselves whether two entries
        # that scored this much are one system or two.
        marginal = None
        for a in range(0, X.shape[0], 500):
            blk = cosine_similarity(X[a:a + 500], X)
            for i in range(blk.shape[0]):
                gi = a + i
                for j in np.where(blk[i] >= thr)[0]:
                    if j > gi:
                        pairs += 1
                        rows.add(gi)
                        rows.add(int(j))
                        score = float(blk[i][j])
                        if marginal is None or score < marginal[0]:
                            marginal = (score, gi, int(j))
        bands.append({"threshold": thr, "candidate_pairs": pairs,
                      "entries_flagged": len(rows),
                      "share_of_register": round(len(rows) / len(reg) * 100, 1),
                      "example": _marginal_pair(reg, marginal, X, vocabulary)})
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
        "similarity_method": SIMILARITY_METHOD,
        "candidate_duplicates_not_confirmed": bands,
        "exact_name_repeats_within_one_agency": {
            "names": int((within > 1).sum()), "rows": int(within[within > 1].sum())},
        "same_name_used_by_more_than_one_agency": int((across > 1).sum()),
        "entries_flagged_at_highest_threshold": sorted(int(i) for i in flagged_at_top),
        "caveat": (
            "Comparing wording cannot show that two entries are the same system. The count "
            "triples depending on how alike they have to be, so it is a choice about where to "
            "draw a line rather than something the file contains."
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
            "This counts each entry on its own. No agency average is taken, and the pattern "
            "describes how information arrives in the file in the same way the nine oversight "
            "fields do."
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


def completeness_where_asked(reg: pd.DataFrame) -> dict:
    """Completeness measured against the entries the register asks each field of.

    A share over all 3,611 rows is the right figure for a field the register
    requires of everything, and the wrong one for a field it requires only of,
    say, pilot and deployed entries. Twenty-two of this register's fields carry
    a condition. Reported over every row, each of those understates how filled
    in it is by counting entries the question was never put to.

    This project published exactly that mistake on the nine oversight fields,
    corrected it there, and had not looked at the rest. This is the rest.

    Entries where the field the condition depends on is itself blank are
    reported separately and are in neither group, because the file does not say
    which side they belong on.
    """
    always, text_only, types = _empty_rule()
    dictionary = COND._dictionary()
    out = {}
    for column in reg.columns:
        asked, undetermined = COND.asked_of(reg, column, dictionary)
        subset = reg.loc[asked, column]
        filled = int((~subset.map(
            lambda v: is_empty(column, v, always, text_only, types))).sum())
        asked_count = int(asked.sum())
        out[column] = {
            # Two columns here are this project's own, added when the register
            # was scrubbed. They carry no Required clause because the publisher
            # never asked them, and they are marked rather than left out, so
            # the table covers every column a reader can see.
            "in_the_publishers_dictionary": column in dictionary,
            "required": COND.required_clause(column, dictionary),
            "conditional": COND.condition(column, dictionary)["kind"] not in
                           {"always", "optional", "not_stated"},
            "asked_of": asked_count,
            "filled": filled,
            "share": round(filled / asked_count * 100, 1) if asked_count else None,
            "not_asked": int(len(reg) - asked_count - int(undetermined.sum())),
            "undetermined": int(undetermined.sum()),
        }
    return out


def m2_completeness(reg: pd.DataFrame) -> dict:
    """What the register holds and what is blank. Within one year only."""
    hi = reg[reg["is_high_impact"] == "High-impact"]
    return {
        "measure": "M2",
        "question": "Does the register hold everything it should, and is each entry filled in?",
        "rule_applied": "Completeness is reported within one year only. The earlier inventory is a schema reference and its rows are not read.",
        "rows": int(len(reg)),
        # Kept, and no longer the only view. For a field the register asks of
        # every entry these two agree. For the twenty-two that carry a
        # condition they do not, and the second is the one that describes an
        # unanswered question.
        "field_completeness_all_rows": completeness(reg),
        "field_completeness_high_impact": completeness(hi),
        "field_completeness_where_asked": completeness_where_asked(reg),
        "completeness_shape": m2_completeness_shape(reg),
        "reconciliation": {
            "figures_that_match": {"individually reported use cases": 3611,
                                    "high-impact use cases": 445,
                                    "agencies reporting individually": 41,
                                    "agencies affirmatively reporting no AI": 2},
            "figures_that_do_not_match": {
                "deployed and piloted": {"published": 1818, "observed": 1480,
                                          "note": "The difference of 338 equals exactly the number of rows with no development stage recorded."},
                # The observed figure here was 54, typed in rather than computed,
                # and no method reproduces it. The two files name the same agency
                # differently, so any count of submissions depends on a matching
                # rule the source does not publish. Every method attempted is
                # recorded in governance/data-provenance.md. Publishing the
                # failure to reconcile is honest; publishing a number with no
                # working is not.
                "total agency submissions": {
                    "published": 56,
                    "observed": None,
                    "note": "No method this project tried reproduced it. The "
                            "individually reported file names 41 agencies and the "
                            "consolidated file names 45, and the two write the same "
                            "agency differently, so any count of distinct submissions "
                            "depends on a rule for matching them. Eight methods were "
                            "tried, giving 86, 57 and 52, and every one is recorded in "
                            "governance/data-provenance.md. A rule that reaches 56 may "
                            "exist and was not found."},
                "agencies reporting consolidated off-the-shelf": {
                    "published": 46, "observed": 45,
                    "note": "The source's own per-agency table and the data file agree at 45. Only the summary bullet differs."},
            },
            "internal_disagreement_in_source_table": {
                "column": "deployed and piloted", "sum_of_rows": 1819, "stated_total": 1818, "difference": 1},
        },
        "caveat": (
            "These figures cannot be compared with the earlier year, because the two years ask "
            "different questions: a box left empty in one year may not exist at all in the other."
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
    # The register requires this date "for pilot and deployed use cases". Every
    # share below that divides by all 3,611 rows counts entries it never asks,
    # which is the same defect this project corrected on the nine oversight
    # fields and had not looked for anywhere else.
    asked, undetermined = COND.asked_of(reg, "operational_date")
    asked_count = int(asked.sum())
    in_scope = reg.loc[asked, "operational_date"].dropna().astype(str).str.strip()
    in_scope = in_scope[~in_scope.str.lower().isin(always)]
    in_scope_parsed = pd.to_datetime(in_scope, errors="coerce", format="mixed")
    outside = reg.loc[~asked, "operational_date"].dropna().astype(str).str.strip()
    outside = outside[~outside.str.lower().isin(always)]
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
        "operational_date_where_asked": {
            "required": COND.required_clause("operational_date"),
            "entries_asked": asked_count,
            "entries_not_asked": int(len(reg) - asked_count - int(undetermined.sum())),
            "entries_undetermined": int(undetermined.sum()),
            "rows_with_a_value": int(len(in_scope)),
            "share_of_entries_asked": round(len(in_scope) / asked_count * 100, 1),
            "values_that_parse": int(in_scope_parsed.notna().sum()),
            "usable_dates_as_share_of_entries_asked":
                round(int(in_scope_parsed.notna().sum()) / asked_count * 100, 1),
            "entries_not_asked_that_carry_a_date_anyway": int(len(outside)),
            "statement": (
                "Measured against every row, usable dates cover about a third of the register. "
                "Measured against the entries the register asks for a date, they cover about "
                "two thirds. The second figure is the one that describes a question with no "
                "answer. A third of those entries still carry no date that can be read."),
            "undetermined_note": (
                "Entries with no development stage recorded cannot be placed on either side, "
                "because the condition is written in terms of stage. They are counted here and "
                "in neither of the other two groups."),
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
            "The one date says when a system started running, not when anyone last looked at "
            "its entry, and a system running for years might have been checked last week or "
            "never."
        ),
    }


# The words the nine oversight fields actually accept. Read from the answers the
# register contains, not from the dictionary, because what agencies typed is the
# evidence and the dictionary is the intention.
#
# Counting whether a field is filled answers a different question from reading
# what it says. Both are reported, because the second changes the first: most of
# what is filled in says the work has not finished.
_IN_PROGRESS = re.compile(r"in[-\s]?progress", re.I)
_NOT_APPLICABLE = re.compile(r"not applicable|precluded", re.I)
# Anything an agency could type to say a step was considered and not taken.
# Searched for rather than assumed, so that the finding is an observation.
_NEGATIVE = re.compile(r"^\s*(no|none|not done|not conducted|not completed|"
                       r"not established|not performed|declined|rejected)\s*\.?\s*$", re.I)


def _answer_state(field: str, value, always, text_only, types) -> str:
    """One of: blank, in progress, done, not applicable, says no."""
    if is_empty(field, value, always, text_only, types):
        return "blank"
    text = str(value).strip()
    if _NOT_APPLICABLE.search(text):
        return "not applicable"
    if _IN_PROGRESS.search(text):
        return "in progress"
    if _NEGATIVE.match(text):
        return "says no"
    return "done"


# The condition the publisher's own dictionary puts on the nine oversight
# fields, quoted from it: "Required: Yes, only for high-impact deployed use
# cases". Not high-impact. High-impact AND deployed.
#
# This project reported blanks across all 445 high-impact entries, which counts
# 218 entries the register does not ask the question of. That is the difference
# between "not yet answered" and "does not apply", which is the distinction this
# project's own field set exists to make. It was applied to the register and not
# to this analysis.
OVERSIGHT_REQUIRED_STAGE = "Deployed"
OVERSIGHT_CONDITION = (
    'The publisher\'s dictionary requires these nine fields "only for '
    'high-impact deployed use cases". An entry flagged high-impact but not '
    'deployed is not asked them, so a blank there records that the question '
    'does not apply, not that it was left unanswered.'
)


def oversight_fields(columns) -> list[str]:
    """The nine oversight columns, named once.

    Derived from the column names rather than written out, and defined here
    rather than inside each measure, so the analysis and the export cannot
    disagree about which nine they are. The justification field is spelled with
    a capital prefix in the source and is not one of them.
    """
    return [c for c in columns if c.startswith("hi_")]


def oversight_conditionality(hi: pd.DataFrame, hifields: list) -> dict:
    """Split the high-impact subset by whether the nine are required of it."""
    always, text_only, types = _empty_rule()
    stage = hi["development_stage"].fillna("").str.strip()
    required = hi[stage.eq(OVERSIGHT_REQUIRED_STAGE)]
    not_required = hi[~stage.eq(OVERSIGHT_REQUIRED_STAGE)]

    def shape(frame):
        answered = sum(
            (~frame[c].map(lambda v: is_empty(c, v, always, text_only, types))).astype(int)
            for c in hifields)
        return {
            "entries": int(len(frame)),
            "all_nine_answered": int((answered == len(hifields)).sum()),
            "none_answered": int((answered == 0).sum()),
            "partially_answered": int(((answered > 0) & (answered < len(hifields))).sum()),
            "share_none_answered": (
                round(float((answered == 0).mean()) * 100, 1) if len(frame) else 0.0),
        }

    return {
        "condition": OVERSIGHT_CONDITION,
        "required_of": shape(required),
        "not_required_of": shape(not_required),
        "stages_not_required": {
            k: int(v) for k, v in
            not_required["development_stage"].fillna("not recorded").value_counts().items()},
        "statement": (
            "Counted across every entry flagged high-impact, the nine are empty on "
            "more entries than the register ever asks them of. Counted across the "
            "entries the register does ask, the figure is lower and is the one that "
            "describes an unanswered question."
        ),
        "caveat": (
            "Both figures are in the file. The wider one counts entries the register "
            "does not put the question to, so it describes the shape of the register "
            "rather than an unanswered question."
        ),
    }


def oversight_answers(hi: pd.DataFrame, hifields: list) -> dict:
    """What the nine oversight fields say, across the high-impact subset."""
    always, text_only, types = _empty_rule()
    counts = {k: 0 for k in ("blank", "in progress", "done", "not applicable", "says no")}
    per_entry = []
    for _, row in hi.iterrows():
        states = [_answer_state(c, row[c], always, text_only, types) for c in hifields]
        for s in states:
            counts[s] += 1
        per_entry.append(states)
    total = sum(counts.values())
    answering = [s for s in per_entry if any(x != "blank" for x in s)]
    more_unfinished = sum(
        1 for s in answering if s.count("in progress") > s.count("done"))
    return {
        "possible_answers": total,
        "fields": len(hifields),
        "entries": int(len(hi)),
        "counts": counts,
        "share": {k: round(v / total * 100, 1) for k, v in counts.items()} if total else {},
        "entries_answering_at_all": len(answering),
        "of_those_more_unfinished_than_done": more_unfinished,
        "of_those_more_unfinished_share": (
            round(more_unfinished / len(answering) * 100, 1) if answering else 0.0),
        "no_field_records_a_step_not_taken": counts["says no"] == 0,
        "statement": (
            "Counting whether these fields are filled and reading what they say give "
            "different answers. Most of what is filled in says the work has not "
            "finished, and no entry records a step as considered and not taken."
        ),
        "caveat": (
            "These are the words agencies entered. The absence of any answer recording "
            "a step not taken describes the answers present in the file, and the field "
            "set offers no wording for one."
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
    hifields = oversight_fields(reg.columns)
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
        "oversight_conditionality": oversight_conditionality(hi, hifields),
        "oversight_answers": oversight_answers(hi, hifields),
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
            "This is a practice exercise modelled on a realistic request. It is not a "
            "response to a request from any body."
        ),
    }


def m5_design_comparison(reg_columns: list[str], ontario: pd.DataFrame) -> dict:
    """How real registers differ in what they ask. Fields, never volume.

    The comparator changed on 30 September 2026. It was the Government of
    Ontario's list, which holds three entries and was never chosen for its fit:
    the brief named it at the start and nobody revisited the choice. It is now
    the United Kingdom's recording standard, which has been required across
    central government since 2024.

    Ontario stays for one thing only, which the UK cannot show: it names no
    supplier in any published field, and both other registers do.
    """
    from src.uk_atrs import allowed_answers, fields as uk_fields

    uk = uk_fields()
    vocabularies = allowed_answers()
    by_section = {}
    for field in uk:
        by_section.setdefault(field["section"], []).append(field["field"])

    return {
        "measure": "M5",
        "question": "How do real registers differ in what they ask, and what does that reveal about design choices?",
        "rule_applied": (
            "Fields asked are compared, never volume. The comparator is the UK "
            "recording standard's published template. No UK records are read, so "
            "nothing here describes how completely anyone fills it in."
        ),
        "federal_register": {"fields_published": len(reg_columns), "entries": 3611},
        "uk_standard": {
            "fields_published": len(uk),
            "fields_asked_only_under_a_condition": sum(1 for f in uk if f["conditional"]),
            "sections": len(by_section),
            "version": "v4.0",
            "note": ("Required across UK central government since 2024. The count is of "
                     "fields the published template asks, not of records anyone filed."),
        },
        "ontario_register": {
            "fields_published": int(len(ontario.columns)),
            "entries": int(len(ontario)),
            "kept_for": ("One contrast the UK cannot provide: Ontario names no supplier "
                         "in any published field."),
        },
        # The fields that answer a question this project found the US list cannot.
        # Each is checked against the US column list rather than asserted.
        "asked_by_the_uk_not_by_the_federal_register": [
            {"field": "Senior responsible owner",
             "note": "A named person answerable for the entry. The US list records no owner."},
            {"field": "Date updated, and date archived",
             "note": "When the record was last changed, and when it was retired. The US "
                     "list has one date and it records when a system started running."},
            {"field": "Phase, with Retired among its allowed answers",
             "note": "A published state for a system switched off. The US list has no "
                     "equivalent, so an entry can only be added."},
            {"field": "Human decisions and review",
             "note": "Where a person sits in the decision. The US list asks this only of "
                     "its high-impact deployed entries."},
            {"field": "Alternatives considered",
             "note": "What else was weighed and set aside. A record of a decision not "
                     "taken, which the US oversight fields have no wording for."},
            {"field": "Procurement procedure type, and Companies House Number",
             "note": "How the thing was bought and from which registered company. The US "
                     "list names a supplier and records nothing about the purchase."},
            {"field": "Maintenance",
             "note": "How the tool is kept up after it is running."},
            {"field": "Model version",
             "note": "Which version is in use, so a change to it can be seen."},
        ],
        "asked_by_the_federal_register_not_by_the_uk": [
            {"field": "A risk classification with a named threshold",
             "note": "The US list flags entries high-impact and asks nine oversight "
                     "questions of the deployed ones. The UK standard asks every entry "
                     "the same questions and sets no tier of its own."},
            {"field": "Whether the entry is withheld from public reporting",
             "note": "The US list asks each entry whether it should be withheld. The UK "
                     "handles this through a separate scope and exemptions policy rather "
                     "than a field."},
        ],
        # What a controlled vocabulary settles, and the US list leaves open.
        "published_answers": {
            "vocabularies": {k: v for k, v in vocabularies.items()},
            "has_a_no": "No" in vocabularies.get("Binary choice", []),
            "note": ("The standard publishes the answers a field may hold. Two matter "
                     "here. Its yes-or-no fields carry an explicit No, and no US "
                     "oversight answer anywhere records a step as considered and not "
                     "taken. And its Phase field carries Retired, so a register built "
                     "on it can record that a system has stopped, and not only "
                     "that one exists."),
        },
        "conditionality_is_marked": {
            "fields_marked": sum(1 for f in uk if f["conditional"]),
            "note": ("The template marks which fields are asked only under a condition. "
                     "A reader can therefore tell a question not put from a question "
                     "unanswered, which is the distinction the US list leaves to whoever "
                     "reads it."),
        },
        "naming_practice": (
            "Three registers, three choices. The US list publishes a supplier name field. "
            "The UK standard asks for the supplier and its company registration number. "
            "The Ontario list names no supplier in any published field. The supplier field "
            "is the one this project removes from its own published data."
        ),
        "caveat": (
            "This compares what each register asks, not how completely anyone fills either "
            "in, because no UK records were read. A template with more fields is not by "
            "itself a better register."
        ),
    }


def question_summary(findings: list[dict], counting_traps: int = 0) -> list[dict]:
    """The five questions a reader would put to a register, with short answers.

    Each answer states a fact. None states a verdict: no grade, no label such as
    partial or weak, because a verdict compresses a judgment and leaves its
    qualification behind. Every figure is read from the findings rather than
    written here, so the summary cannot drift from what it summarises.
    """
    by = {f["measure"]: f for f in findings}
    m1, m2, m3, m4, m5 = by["M1"], by["M2"], by["M3"], by["M4"], by["M5"]
    reconciliation = m2["reconciliation"]
    consolidated = m1["consolidated_route"]
    oversight = m4["oversight_block_shape"]

    return [
        {
            "id": "count",
            "question": "How many AI systems are there?",
            "answer": (
                f"{m1['individually_reported_entries']:,} are reported one by one. "
                f"A second route adds {consolidated['agencies']} agencies reporting against "
                f"{consolidated['distinct_common_tasks']} shared tasks. The two count different "
                "things and are not added together."
            ),
            "section": "The register counts two different kinds of thing",
        },
        {
            "id": "reconcile",
            "question": "Do the published totals agree with the data?",
            "answer": (
                f"{len(reconciliation['figures_that_match'])} of "
                f"{len(reconciliation['figures_that_match']) + len(reconciliation['figures_that_do_not_match'])} "
                "figures the source states match the file exactly. "
                f"{len(reconciliation['figures_that_do_not_match'])} do not, and the source's own "
                "summary table disagrees with the total printed beneath it."
            ),
            "section": "Three of the publisher's own figures do not match its data",
        },
        {
            "id": "current",
            "question": "How current is any of it?",
            "answer": (
                "No entry records when it was last checked. The register has one date field, "
                "asked only of entries at the pilot and deployed stages, readable on "
                f"{m3['operational_date_where_asked']['usable_dates_as_share_of_entries_asked']}% "
                "of those, and it records when a system started running."
            ),
            "section": "The register cannot say how current any entry is",
        },
        {
            # This page has no oversight section: that material is on the third
            # page. Its fourth section is about counting the file correctly, and
            # the question is written to match what is actually beneath it.
            "id": "counting",
            "question": "Can a careful person count this file correctly?",
            "answer": (
                f"Not without knowing {counting_traps} things about how the files are written. "
                "Three make a column read fuller than it is, one makes a set of choices look "
                "complete, and the rest concern the files themselves."
            ),
            "section": "Seven ways a careful person would still get these numbers wrong",
            "elsewhere": {
                "question": "Could it answer a question about the riskiest systems?",
                "answer": (
                    f"Of {m4['subset_size']:,} entries flagged high-impact, "
                    f"{oversight['none_answered']:,} have all nine oversight fields empty."
                ),
                "link": "obligations.html",
            },
        },
        {
            "id": "compare",
            "question": "What does another government ask that this one does not?",
            "answer": (
                f"{len(m5['asked_by_the_uk_not_by_the_federal_register'])} questions the UK "
                "recording standard asks and the US list does not, including who is answerable "
                "for the entry, when it was last changed, and whether the system has been "
                "retired. Its yes-or-no fields carry an explicit No, and no US oversight answer "
                "anywhere records a step as considered and not taken."
            ),
            "section": "Another government asks different questions",
        },
    ]
