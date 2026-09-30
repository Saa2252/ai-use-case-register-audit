"""The worked example obeys the rule the page states beside it.

Page four sets out a convention: every field distinguishes answered, the
question does not apply, not yet answered and withheld, and no field records an
absence as ordinary text. The worked example on the same page broke it. All
nine oversight questions sat in one box as a paragraph, and two of them said in
words that there was no answer: "not applicable at this classification" and
"not yet carried out". The rule was stated and the example contradicted it, on
the same screen.

Nothing caught it, because the example is fictional and every other check on
this repository reads either the published data or the copy. This one reads the
example against the rule.

Four checks:

1. Every row carries a state the convention names.
2. A row that is not answered carries no answer. The state is the record.
3. No answer anywhere contains a phrase that records an absence in words.
4. The nine oversight questions in the example are the nine the field names,
   in the order the field names them.

Verified by planting the failure: putting the original field-8 paragraph back
into `scripts/build_fieldset.py` fails checks 3 and 4 and names the phrases.
"""

import json
import sys

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src.fieldset import FIELDS, STATES  # noqa: E402

FIELDSET = REPO_ROOT / "docs" / "data" / "fieldset.json"

# Ways of writing "there is no answer here" as though it were an answer. Each
# is a state the field set already has, so any of them inside a value means the
# state was thrown away and re-recorded as prose.
ABSENCE_IN_WORDS = [
    "not applicable",
    "n/a",
    "not yet",
    "not available",
    "not carried out",
    "not recorded",
    "not assessed",
    "no answer",
    "none recorded",
    "unknown",
    "to be confirmed",
]


def _panel_two() -> dict:
    return json.loads(FIELDSET.read_text(encoding="utf-8"))["panel_two"]


def _all_rows(panel: dict) -> list:
    rows = []
    for row in panel["rows"]:
        rows.append(("", row))
        for sub in row.get("sub_rows", []):
            rows.append((row["field"] + " / ", sub))
    return rows


def test_every_row_carries_a_state_the_convention_names():
    wrong = [f"{where}{row['field']}: {row.get('state')!r}"
             for where, row in _all_rows(_panel_two())
             if row.get("state") not in STATES]
    assert not wrong, (
        "the worked example uses a state the convention does not name:\n" + "\n".join(wrong)
    )


def test_a_row_that_is_not_answered_carries_no_answer():
    wrong = [f"{where}{row['field']}"
             for where, row in _all_rows(_panel_two())
             if row["state"] != "answered" and row.get("value")]
    assert not wrong, (
        "a row is marked as having no answer and carries words anyway, which is "
        "the state and the prose saying different things:\n" + "\n".join(wrong)
    )


def test_no_answer_records_an_absence_as_ordinary_text():
    found = []
    for where, row in _all_rows(_panel_two()):
        value = (row.get("value") or "").lower()
        for phrase in ABSENCE_IN_WORDS:
            if phrase in value:
                found.append(f"{where}{row['field']} says '{phrase}' inside its answer")
    assert not found, (
        "the worked example records an absence as ordinary text, which is the one "
        "thing the convention on the same page says no field does:\n" + "\n".join(found)
    )


def test_the_nine_are_the_nine_the_field_names():
    field = next(f for f in FIELDS if f.get("sub_fields"))
    row = next(r for r in _panel_two()["rows"] if r.get("sub_rows"))
    shown = [s["field"] for s in row["sub_rows"]]
    assert shown == field["sub_fields"], (
        "the worked example's oversight questions have drifted from the field that "
        f"names them:\n  field: {field['sub_fields']}\n  example: {shown}"
    )
