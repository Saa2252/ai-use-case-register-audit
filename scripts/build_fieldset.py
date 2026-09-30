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

from src.fieldset import (  # noqa: E402
    EMPTY_CONVENTION, EVIDENCE, EVIDENCE_WITHHELD, FIELDS, STATES)
from src.disclaimer import REPOSITORY_URL  # noqa: E402
from src.statements import apply as apply_statements  # noqa: E402
from src.measures import _empty_rule, is_empty  # noqa: E402

DERIVED = REPO_ROOT / "data" / "derived"
DOCS_DATA = REPO_ROOT / "docs" / "data"


def judgment_calls() -> int:
    """Count the judgment calls the README sets out.

    The landing page names this number. Counting the headings here means a
    judgment call added to the README cannot leave the page saying the old
    figure, which is what happened when the count was typed into the script.
    """
    lines = (REPO_ROOT / "README.md").read_text(encoding="utf-8").splitlines()
    inside = False
    count = 0
    for line in lines:
        if line.startswith("## "):
            inside = "judgment call" in line.lower()
            continue
        if inside and line.startswith("### "):
            count += 1
    return count

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


# Which fields the register only asks under a condition, and what the condition
# is. Quoted from the publisher's dictionary, which says of each of the nine
# oversight fields: "Required: Yes, only for high-impact deployed use cases".
#
# Without this the panel marked a blank on a not-high-impact entry as "asked,
# left empty". That is the wrong one of the four states: the register does not
# ask it of that entry at all. The distinction is the reason this field set
# exists, and it was applied to the register and not to this page.
CONDITIONAL_FIELDS = {
    "The nine oversight questions, each with its own explicit states": {
        "applies": lambda row: (
            str(row.get("is_high_impact", "")).strip() == "High-impact"
            and str(row.get("development_stage", "")).strip() == "Deployed"),
        "why_not": ("The register asks these only of high-impact entries that are "
                    "deployed. This entry is neither, so the question is not put to it."),
    },
}


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
        condition = CONDITIONAL_FIELDS.get(field["name"])
        if condition and not condition["applies"](row):
            rows.append({"field": field["name"], "value": None, "state": "does_not_apply",
                         "label": condition["why_not"]})
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


# The nine oversight answers for the made-up entry, keyed to the sub-questions
# named on the field itself so the example cannot drift from the field it fills.
#
# Each is a state and, where the state is "answered", a value. An answer that
# does not exist carries no words at all. The earlier version of this panel put
# all nine in one box as a paragraph, with "not applicable at this
# classification" and "not yet carried out" written into the prose. That is an
# absence recorded as ordinary text, which is the one thing the convention on
# this page says no field does. The example contradicted the rule it existed to
# demonstrate.
NINE_ANSWERS = {
    "Tested before deployment": {
        "state": "answered",
        "value": "Yes. Tested on a sample of past complaints before release."},
    "Impact assessment completed": {
        "state": "answered",
        "value": "Yes. Completed 4 February 2026."},
    "Potential impacts identified": {
        "state": "answered",
        "value": "Yes. A reply in the wrong tone, and delay while the tool is unavailable."},
    "Independent review conducted": {
        "state": "does_not_apply",
        "ground": "This authority requires independent review only of systems it "
                  "classifies high impact. This one is not."},
    "Ongoing monitoring in place": {
        "state": "answered",
        "value": "Yes. Monthly sampling of replies that were sent."},
    "Training established for operators": {
        "state": "answered",
        "value": "Yes. Completed for every caseworker who uses it."},
    "Fail-safe in place": {
        "state": "answered",
        "value": "Yes. Replies can be written and sent without the tool."},
    "Appeal process in place": {
        "state": "answered",
        "value": "Yes. The existing complaints process is unchanged and is the route of appeal."},
    "Consultation with the people it affects": {
        "state": "not_yet_answered"},
}


def nine_answers() -> list:
    """The nine, in the order the field names them, each with its own state."""
    field = next(f for f in FIELDS if f.get("sub_fields"))
    rows = []
    for name in field["sub_fields"]:
        answer = NINE_ANSWERS.get(name)
        if answer is None:
            raise SystemExit(f"the made-up entry has no answer for '{name}'")
        row = {"field": name, "state": answer["state"],
               "value": answer.get("value"), "ground": answer.get("ground")}
        if row["state"] == "answered" and not row["value"]:
            raise SystemExit(f"'{name}' is marked answered and carries no answer")
        if row["state"] != "answered" and row["value"]:
            raise SystemExit(f"'{name}' is not answered and carries words anyway")
        rows.append(row)
    return rows


def panel_two() -> dict:
    """A fictional organisation. No real system, no real data.

    Every row carries one of the states in src.fieldset.STATES. A row that is
    not answered carries no value, because the state is the record. Where a
    state needs a reason, the reason sits in its own place rather than inside
    the answer.
    """
    rows = [
        {"field": "Entry identifier", "state": "answered", "value": "CTA-0041"},
        {"field": "Date this entry was last checked", "state": "answered",
         "value": "12 March 2026"},
        {"field": "What changed since the last check", "state": "answered",
         "value": "The model version. The responsible office, the data it draws on, what it "
                  "is used for and how far it acts without a person are all unchanged."},
        {"field": "Acts without a person reviewing the output", "state": "answered",
         "value": "No. It does not act on its own: every draft reply is read by a caseworker "
                  "before anything is sent."},
        {"field": "Where a person reviews it", "state": "answered",
         "value": "At the point of sending. The caseworker may edit the draft or discard it."},
        {"field": "Impact classification, with an explicit option for not yet assessed",
         "state": "answered",
         "value": "Assessed, and not high impact. The output is a draft, and the decision that "
                  "reaches the passenger is the caseworker's."},
        {"field": "Withheld from public reporting, and on what ground", "state": "answered",
         "value": "No. Nothing in this entry is held back."},
        {"field": "The nine oversight questions, each with its own explicit states",
         "state": "answered", "value": None, "sub_rows": nine_answers()},
        {"field": "What this entry counts as one of", "state": "answered",
         "value": "One system."},
        {"field": "Who completed this entry, and when", "state": "answered",
         "value": "Customer Services, 12 March 2026."},
    ]
    return {
        "organisation": "A fictional city transport authority",
        "system": "A fictional tool that drafts replies to passenger complaints",
        "label": "Fictional throughout. No real organisation, no real system, no real data. "
                 "It exists to show the field set filled in.",
        # What the reader should take from the right-hand form. It is not that
        # every box holds words. It is that every box holds a state.
        "reading": "Every box on this form is resolved. Most carry an answer. Among the nine "
                   "oversight questions, one is not put to this entry and one has been put and "
                   "has no answer yet. Neither of those is written as words inside an answer: "
                   "each is a state the field holds, which is what lets the two be told apart.",
        "state_not_shown": ("Nothing on this entry is held back, so the state for a withheld "
                            "answer does not appear on it. The field that records withholding "
                            "is answered No."),
        "rows": rows,
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
    "does_not_apply": "not asked of this entry",
}

STATE_LINE = {
    "from_source": "The published register records this.",
    "not_collected": "The published register does not collect this.",
    "blank_in_source": "The published register asks this, and this entry leaves it empty.",
    "does_not_apply": "The published register does not ask this of an entry like this one.",
}


def slots_caption(headline: dict) -> str:
    """What the strip of marks says, in words.

    The strip used to caption every unanswered box as "left blank", which
    contradicted the paragraph beside it: on this entry none was asked and left
    blank. The caption is built from the same split the marks are drawn from,
    so the picture and the words cannot disagree.
    """
    parts = [f"{headline['a_real_entry_can_fill']} of {headline['fields']} boxes carry "
             "an answer from the published entry."]
    if headline["not_collected"]:
        parts.append(f"That register does not collect {headline['not_collected']} of them.")
    if headline["does_not_apply"]:
        parts.append(f"{headline['does_not_apply']} it collects and does not put to an "
                     "entry like this one.")
    empty = headline["asked_and_left_empty"]
    parts.append(f"{empty} were asked and left empty." if empty
                 else "None was asked and left empty.")
    return " ".join(parts)


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
                 "the left. The second form is one made-up organisation giving every "
                 "box a definite state, which is not the same as writing words in "
                 "every box."),
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
            "sources": "The 2025 US federal AI use case inventory, read in full. The "
                       "United Kingdom's recording standard, read as a published "
                       "field template and not as records. The Government of "
                       "Ontario's list, kept for one observation about supplier "
                       "naming.",
            "downloaded": "2026-09-22, and the UK template on 2026-09-30",
            "snapshot": "A single point in time, each file recorded by SHA-256 hash in "
                        "governance/data-provenance.md.",
        },
        # Four of these describe what the audit could see. The last two are
        # about this field set itself, and are here because the README now says
        # the audit is the method and the field set is the result. A result
        # should carry what it has not been put through.
        "limits": [
            "One register, in one year.",
            "Read from outside, with no access to how any agency works.",
            "Built from what a published file shows, which is not everything an organisation knows.",
            "Not tested against anyone who keeps a register.",
            "This field set has not been used to record anything real. Every "
            "question on it answers something the audit found, and none of them "
            "has been put in front of a person asked to fill it in.",
            "Nothing here compares one organisation with another. That is a "
            "choice, and it has a cost: the question a reader is most likely to "
            "arrive with is the one this project will not answer.",
        ],
        "fields": fields_with_figures(),
        "convention": EMPTY_CONVENTION,
        "evidence": evidence_strip(),
        "evidence_withheld": EVIDENCE_WITHHELD,
        # Empty until the owner creates the repository. The page renders a link
        # only when it carries an address, so nothing points at a page that is
        # not there yet.
        # Two things a reader should meet before they take the field set as a
        # conclusion. Both were raised from outside, both are held here rather
        # than typed into the page, and their figures are read from the
        # findings like every other number.
        "timing": {
            "heading": "Some of these blanks may be a clock, not a gap",
            "lead": "A blank can mean nobody recorded the answer. It can also mean "
                    "the work is under way and the answer does not exist yet. This "
                    "project cannot tell those apart, and the figures lean toward "
                    "the second more than the headline suggests.",
            "in_progress_share": _resolve(_findings_store(), "M4.oversight_answers.share.in progress"),
            "entries_answering": _resolve(_findings_store(), "M4.oversight_answers.entries_answering_at_all"),
            "more_unfinished": _resolve(_findings_store(), "M4.oversight_answers.of_those_more_unfinished_than_done"),
            "reading": "of every answer the nine oversight fields contain says a "
                       "step is under way rather than finished.",
            "what_this_project_will_not_say": "The register's own dictionary cites the "
                "White House memorandum these fields come from, and that memorandum "
                "sets dates by which agencies are to document this work. This project "
                "does not state those dates, because it cannot check them against any "
                "file it holds, and it publishes nothing it cannot check. What it can "
                "say is that the file records no date by which any answer was due, so "
                "an outside reader cannot tell a gap from a clock.",
            "consequence": "Read the blanks as what reached the file on the day it was "
                           "downloaded, not as work that was not done.",
        },
        "not_covered": {
            "heading": "What this field set does not do",
            "lead": "These ten questions describe what a register should record. They "
                    "do not describe how one is run, and a register that is not run is "
                    "a document rather than a control.",
            "missing": [
                {"name": "A named person accountable for each entry",
                 "why": "A field with no owner is nobody's to keep current."},
                {"name": "What forces an update, and how often one is due",
                 "why": "Two of the ten ask when an entry was last checked and what "
                        "changed. Neither makes anyone check it."},
                {"name": "Approval gates tied to buying and starting a system",
                 "why": "A register filled in after the fact records decisions rather "
                        "than shaping them."},
                {"name": "A state for a system that has been switched off",
                 "why": "Without one, a register grows and never empties."},
                {"name": "A link from each answer to the evidence behind it",
                 "why": "Every field here records a claim. None records where the "
                        "claim can be checked."},
            ],
            "coverage": "There is also a limit no register design can solve from "
                        "outside. A published list shows what an organisation wrote "
                        "down. It cannot show systems nobody declared, or the AI "
                        "features that arrive inside software bought for something "
                        "else. Both are outside anything this project can see.",
            "comparators_lead": "The comparison here is the United Kingdom's "
                                "recording standard. Two other places ask for similar "
                                "records and neither was read, so the ten fields are "
                                "not compared to either.",
            "comparators": [
                {"name": "The European Union's rule on entering AI in a public database",
                 "what": "Before certain AI systems can be used in the EU, they have to "
                         "be entered in a database anyone can look at.",
                 "why": "It is a register with a different purpose: it decides who has "
                        "to appear on it, which neither the US list nor the UK "
                        "standard does."},
                {"name": "The international standard for managing AI, ISO/IEC 42001",
                 "what": "A published standard describing how an organisation should "
                         "run its AI oversight. An organisation can be checked against "
                         "it by an outside auditor.",
                 "why": "It covers the part this field set leaves out, which is how a "
                        "register is kept up rather than what it records."},
            ],
            "consequence": "Treat this as a proposal about what a register records, "
                           "traced to one published file and compared against one "
                           "published standard. It is not an operating "
                           "model, and it has not been checked against the standards "
                           "that set one.",
        },
        # The same corrections the findings carry, so a page reading either
        # file renders one text rather than two that can drift.
        "corrections": json.loads(
            (DERIVED / "findings.json").read_text(encoding="utf-8"))["corrections"],
        "repository_url": REPOSITORY_URL,
        "judgment_calls": judgment_calls(),
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
        "does_not_apply": states.get("does_not_apply", 0),
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
    # The nine oversight fields are required of high-impact entries that are
    # deployed, which the publisher's dictionary states and this project had not
    # applied. Counting blanks across all 445 counts 218 entries the register
    # never puts the question to. The opening now states the figure for the
    # entries the register does ask, and the page gives both.
    payload["lead"] = {
        "entries": _resolve(store, "M2.rows"),
        "high_impact": _resolve(store, "M4.subset_size"),
        "asked_the_nine": _resolve(store, "M4.oversight_conditionality.required_of.entries"),
        "no_oversight": _resolve(store, "M4.oversight_conditionality.required_of.none_answered"),
        "share_no_oversight": _resolve(
            store, "M4.oversight_conditionality.required_of.share_none_answered"),
        "no_oversight_all_flagged": _resolve(store, "M4.oversight_block_shape.none_answered"),
    }
    for key, value in payload["lead"].items():
        if value is None:
            raise SystemExit(f"the opening needs {key} and the findings do not carry it")

    payload["steps"] = reading_steps(payload["panel_one"], payload["panel_two"])
    for row in payload["panel_one"]["rows"]:
        row["short"] = SHORT_STATE[row["state"]]
    # The word for each state travels with the row rather than being written in
    # the page script, so the states the convention names and the states the
    # example prints are the same words.
    for row in payload["panel_two"]["rows"]:
        row["state_word"] = STATES[row["state"]]
        for sub in row.get("sub_rows", []):
            sub["state_word"] = STATES[sub["state"]]
    payload["headline"]["slots_caption"] = slots_caption(payload["headline"])

    (DERIVED / "fieldset.json").write_text(json.dumps(payload, indent=2) + "\n")
    (DOCS_DATA / "fieldset.json").write_text(json.dumps(payload, indent=2) + "\n")

    counts = {}
    for row in payload["panel_one"]["rows"]:
        counts[row["state"]] = counts.get(row["state"], 0) + 1
    print(f"fields: {len(payload['fields'])}")
    print(f"panel one, entry {ENTRY_ID}: {counts}")


if __name__ == "__main__":
    main()
