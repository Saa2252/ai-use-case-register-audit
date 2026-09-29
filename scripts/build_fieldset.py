"""Build the page-four data: the field set and the two worked panels.

Panel one is generated from the published file. Every value in it is read from
the register, never inferred, estimated or filled with something plausible. A
field the source does not collect is marked as such. A field the source asks and
leaves empty is marked differently, because those are different facts.

Panel two is fictional and is labelled as fictional everywhere it appears.
"""

import json
import sys
import warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
warnings.filterwarnings("ignore")

import pandas as pd  # noqa: E402

from src.fieldset import EMPTY_CONVENTION, EVIDENCE, EVIDENCE_WITHHELD, FIELDS  # noqa: E402
from src.disclaimer import REPOSITORY_URL  # noqa: E402
from src.statements import apply as apply_statements  # noqa: E402
from src.measures import _empty_rule, is_empty  # noqa: E402

DERIVED = REPO_ROOT / "data" / "derived"
DOCS_DATA = REPO_ROOT / "docs" / "data"

# Which source column, if any, answers each proposed field.
SOURCE_COLUMN = {
    "Entry identifier": ["id"],
    "Date this entry was last checked": [],
    "What changed since the last check": [],
    "Acts without a person reviewing the output": [],
    "Where a person reviews it": [],
    "Impact classification, with an explicit option for not yet assessed": ["is_high_impact"],
    "Withheld from public reporting, and on what ground": ["is_withheld"],
    "The nine oversight questions, each with its own explicit states": [
        "hi_testing_conducted", "hi_assessment_completed", "hi_potential_impacts",
        "hi_independent_review", "hi_ongoing_monitoring", "hi_training_established",
        "hi_failsafe_presence", "hi_appeal_process", "hi_public_consultation"],
    "What this entry counts as one of": [],
    "Who completed this entry, and when": [],
}

NOT_COLLECTED = "the source register does not collect this"
BLANK_IN_SOURCE = "the source register asks this and this entry leaves it empty"

ENTRY_ID = "FRB-0055"


def panel_one(register: pd.DataFrame) -> dict:
    always, text_only, types = _empty_rule()
    row = register.loc[register["id"] == ENTRY_ID].iloc[0]
    rows = []
    for field in FIELDS:
        columns = SOURCE_COLUMN.get(field["name"], [])
        if not columns:
            rows.append({"field": field["name"], "value": None, "state": "not_collected",
                         "label": NOT_COLLECTED})
            continue
        values = []
        for column in columns:
            if not is_empty(column, row[column], always, text_only, types):
                values.append(f"{column}: {row[column]}" if len(columns) > 1 else str(row[column]))
        if values:
            rows.append({"field": field["name"], "value": "; ".join(values), "state": "from_source",
                         "label": None})
        else:
            rows.append({"field": field["name"], "value": None, "state": "blank_in_source",
                         "label": BLANK_IN_SOURCE})
    return {
        "entry_id": ENTRY_ID,
        "use_case_name": str(row["use_case_name"]),
        "agency": str(row["agency_name"]),
        "why_this_entry": "An ordinary entry, not flagged high-impact, describing internal data "
                          "quality work. Chosen because nothing about it is sensitive.",
        "rule": "Every value here is read from the published file. Nothing is inferred, estimated "
                "or filled with a plausible answer. Where the source collects nothing, the row is "
                "marked as such. Where the source asks and this entry is empty, the row is marked "
                "differently, because those are different facts.",
        "rows": rows,
    }


def panel_two() -> dict:
    """A fictional organisation. No real system, no real data."""
    return {
        "organisation": "A fictional city transport authority",
        "system": "A fictional tool that drafts replies to passenger complaints",
        "label": "Fictional throughout. No real organisation, no real system, no real data. "
                 "It exists to show the field set filled in.",
        "rows": [
            {"field": "Entry identifier", "value": "CTA-0041, unchanged since first registered"},
            {"field": "Date this entry was last checked", "value": "12 March 2026"},
            {"field": "What changed since the last check",
             "value": "Model version changed. The responsible office, data sources, purpose and "
                      "degree of autonomy are unchanged."},
            {"field": "Acts without a person reviewing the output",
             "value": "No. Every draft reply is read by a caseworker before it is sent."},
            {"field": "Where a person reviews it",
             "value": "At the point of sending. The caseworker may edit or discard the draft."},
            {"field": "Impact classification, with an explicit option for not yet assessed",
             "value": "Assessed, not high impact. The output is a draft, and the decision that "
                      "reaches the passenger is the caseworker's."},
            {"field": "Withheld from public reporting, and on what ground",
             "value": "No. Published in full."},
            {"field": "The nine oversight questions, each with its own explicit states",
             "value": "Tested before deployment: yes. Impact assessment: completed. Potential "
                      "impacts: recorded. Independent review: not applicable at this "
                      "classification. Monitoring: monthly sampling of sent replies. Operator "
                      "training: completed for all caseworkers. Fail-safe: replies can be sent "
                      "without the tool. Appeal: the existing complaints process is unchanged. "
                      "Consultation: not yet carried out."},
            {"field": "What this entry counts as one of",
             "value": "One system."},
            {"field": "Who completed this entry, and when",
             "value": "Customer Services, 12 March 2026."},

        ],
    }


def _findings_store() -> dict:
    """Every finding, keyed the same way the site keys them."""
    store = {}
    one = json.loads((DERIVED / "findings.json").read_text())
    for f in one.get("findings", []):
        store[f["measure"]] = f
    two = json.loads((DERIVED / "reusability_findings.json").read_text())
    for f in two.get("findings", []):
        store[f["id"]] = f
    return store


def _resolve(store: dict, path: str):
    node = store
    for key in path.split("."):
        if node is None:
            return None
        node = node.get(key) if isinstance(node, dict) else None
    return node


def evidence_strip() -> list:
    """Resolve each evidence figure here rather than in the browser.

    The landing page used to download every finding on the site to read five
    numbers out of them. Resolving at build time keeps the numbers computed from
    the data and published from data/derived, and drops two files the reader
    does not otherwise need. tests/test_evidence_figures.py re-reads the
    findings and fails if any figure here has drifted from its source.
    """
    store = _findings_store()
    strip = []
    for item in EVIDENCE:
        value = _resolve(store, item["path"])
        if value is None:
            raise SystemExit(f"evidence path not found in the findings: {item['path']}")
        row = dict(item)
        row["value"] = value
        if item.get("of"):
            of = _resolve(store, item["of"])
            if of is None:
                raise SystemExit(f"evidence denominator not found: {item['of']}")
            row["of_value"] = of
        strip.append(row)
    return strip


# What each state means, in one line. The reading steps are built from these, so
# the narration beside the panels can never say something the row does not.
# The caption printed under an empty box on the drawn form. Short enough to sit
# under a box without becoming the content of it. Derived from the row's state,
# so a caption cannot say something the row does not.
SHORT_STATE = {
    "from_source": "",
    "not_collected": "not collected by this register",
    "blank_in_source": "asked, left empty",
}

STATE_LINE = {
    "from_source": "The published register records this.",
    "not_collected": "The published register does not collect this.",
    "blank_in_source": "The published register asks this, and this entry leaves it empty.",
}


def reading_steps(one: dict, two: dict) -> list:
    """One step per field, narrating the real entry row by row.

    Every line is derived from the row's own state, not written out here, so a
    step cannot drift from the panel it points at. The last step states the
    count, computed the same way as the headline.
    """
    steps = []
    for index, row in enumerate(one["rows"]):
        steps.append({
            "row": index,
            "field": row["field"],
            "line": STATE_LINE[row["state"]],
            "state": row["state"],
        })
    filled = sum(1 for r in one["rows"] if r["state"] == "from_source")
    steps.append({
        "row": None,
        "field": "Of the ten, this is what carries a value",
        "line": (f"{filled} of {len(one['rows'])} boxes carry a value from the published "
                 f"register. The other {len(one['rows']) - filled} are the empty boxes on "
                 "the left. The second form is one made-up organisation filling in "
                 "every one."),
        "state": "summary",
    })
    return steps


def fields_with_figures() -> list:
    """Fill the placeholders in the field descriptions from the findings.

    One figure in these descriptions was typed by hand and was wrong: the
    identifier repeat count read "thirteen" where the file holds twelve. Any
    number in this prose is now resolved from the published findings.
    """
    store = _findings_store()
    repeated = _resolve(store, "R3.figures.identifier_values_on_more_than_one_row")
    if repeated is None:
        raise SystemExit("the findings carry no identifier repeat count")
    out = []
    for field in FIELDS:
        row = dict(field)
        row["us_2025"] = row["us_2025"].replace("{repeated_ids}", str(repeated))
        if row.get("rests_on"):
            row["rests_on"] = apply_statements(row["rests_on"])
        out.append(row)
    return out


def main() -> None:
    register = pd.read_csv(DERIVED / "register_2025_scrubbed.csv", dtype=str, low_memory=False)
    payload = {
        "what_this_is": "The first three pages describe the register as published. This page is "
                        "the author's own view: what they would build, given what the audit found.",
        "based_on": {
            "sources": "Two published registers: the 2025 US federal AI use case inventory and "
                       "the Government of Ontario's list.",
            "downloaded": "2026-09-22",
            "snapshot": "A single point in time, each file recorded by SHA-256 hash in "
                        "governance/data-provenance.md.",
        },
        "limits": [
            "One register, in one year.",
            "Read from outside, with no access to how any agency works.",
            "Built from what a published file shows, which is not everything an organisation knows.",
            "Not tested against anyone who keeps a register.",
        ],
        "fields": fields_with_figures(),
        "convention": EMPTY_CONVENTION,
        "evidence": evidence_strip(),
        "evidence_withheld": EVIDENCE_WITHHELD,
        # Empty until the owner creates the repository. The page renders a link
        # only when it carries an address, so nothing points at a page that is
        # not there yet.
        "repository_url": REPOSITORY_URL,
        "panel_one": panel_one(register),
        "panel_two": panel_two(),
    }
    states = {}
    for row in payload["panel_one"]["rows"]:
        states[row["state"]] = states.get(row["state"], 0) + 1
    cannot_fill = sum(1 for r in payload["panel_one"]["rows"] if r["state"] != "from_source")
    payload["headline"] = {
        "fields": len(FIELDS),
        "a_real_entry_can_fill": len(FIELDS) - cannot_fill,
        "a_real_entry_cannot_fill": cannot_fill,
        # Split the seven it cannot fill, because a reader arriving on this page
        # with no other context needs to know why the number is three. Six are
        # not collected by the register at all; one is asked and left empty.
        "not_collected": states.get("not_collected", 0),
        "asked_and_left_empty": states.get("blank_in_source", 0),
        "entry": payload["panel_one"]["entry_id"],
        "entry_agency": payload["panel_one"]["agency"],
        # The size of the file this entry comes from, read from the findings so
        # the landing page can name its source without a typed-in number.
        "register_entries": _resolve(_findings_store(), "M2.rows"),
    }
    # The figures the opening states, before anything about this project. Read
    # from the findings so the first thing a stranger reads is computed, not
    # written out.
    store = _findings_store()
    payload["lead"] = {
        "entries": _resolve(store, "M2.rows"),
        "high_impact": _resolve(store, "M4.subset_size"),
        "no_oversight": _resolve(store, "M4.oversight_block_shape.none_answered"),
    }
    for key, value in payload["lead"].items():
        if value is None:
            raise SystemExit(f"the opening needs {key} and the findings do not carry it")

    payload["steps"] = reading_steps(payload["panel_one"], payload["panel_two"])
    for row in payload["panel_one"]["rows"]:
        row["short"] = SHORT_STATE[row["state"]]

    (DERIVED / "fieldset.json").write_text(json.dumps(payload, indent=2) + "\n")
    (DOCS_DATA / "fieldset.json").write_text(json.dumps(payload, indent=2) + "\n")

    counts = {}
    for row in payload["panel_one"]["rows"]:
        counts[row["state"]] = counts.get(row["state"], 0) + 1
    print(f"fields: {len(payload['fields'])}")
    print(f"panel one, entry {ENTRY_ID}: {counts}")


if __name__ == "__main__":
    main()
