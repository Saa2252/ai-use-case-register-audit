"""No page renders a raw column name to a reader.

The register names its columns for a database. Shown with the underscores taken
out, one of them reads as a greeting: the prefix marking the nine questions
asked only of high-impact entries turns hi_public_consultation into
"hi public consultation".

Every column therefore has a published label, and the scripts look it up rather
than transforming the column name themselves.
"""

import json
import re
import sys

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src.labels import FIELD_GROUPS, FIELD_LABELS, GROUP_OF  # noqa: E402

DOCS = REPO_ROOT / "docs"


def test_every_published_column_has_a_label():
    published = json.loads((DOCS / "data" / "register_full.json").read_text())["fields"]
    missing = [c for c in published if c not in FIELD_LABELS]
    assert not missing, f"published columns with no reader-facing label: {missing}"


def test_labels_are_published_for_the_pages():
    path = DOCS / "data" / "field_labels.json"
    assert path.exists(), "field_labels.json is not published"
    published = json.loads(path.read_text())
    assert published["labels"] == FIELD_LABELS, (
        "the published labels have drifted from the single source")


def test_no_script_derives_a_label_from_a_column_name():
    """A script that strips underscores is inventing a label rather than using one.

    Falling back to that when a label is genuinely missing is allowed. Using it
    as the primary path is what produced the greeting.
    """
    offenders = []
    for script in sorted((DOCS / "assets").glob("*.js")):
        text = script.read_text()
        for match in re.finditer(r'replace\(/_/g, " "\)', text):
            line_number = text[:match.start()].count("\n") + 1
            line = text.splitlines()[line_number - 1]
            if "LABELS[column]" in line or "||" in line:
                continue          # the documented fallback
            offenders.append(f"{script.name}:{line_number}")
    assert not offenders, (
        "scripts building a label out of a column name instead of looking it up:\n"
        + "\n".join(offenders))


def test_no_label_starts_with_the_high_impact_prefix():
    bad = [c for c, text in FIELD_LABELS.items() if re.match(r"^hi\b", text, re.I)]
    assert not bad, f"labels that still read as the raw prefix: {bad}"


def test_conditional_fields_carry_the_condition_they_are_asked_under():
    """A label loses the condition the column name carried in its prefix.

    The nine oversight questions are asked only of entries that are flagged
    high-impact **and deployed**, and the justification field only of entries
    presumed high-impact and then determined not to be. Those are different
    populations, so they are different groups. Replacing the prefix with a
    readable label drops that unless the group is stated.

    The group said "flagged high-impact" and stopped there until 30 September
    2026. Half a condition, stated above a table of per-question shares, is how
    every one of those shares came to be divided by 445 rather than by the 227
    the register asks.
    """
    published = json.loads((DOCS / "data" / "field_labels.json").read_text())
    assert published["group_of"] == GROUP_OF, "published groups have drifted from the source"

    prefixed = [c for c in FIELD_LABELS if c.lower().startswith("hi_")]
    ungrouped = [c for c in prefixed if c not in GROUP_OF]
    assert not ungrouped, (
        f"columns whose name carries a condition but whose label does not: {ungrouped}")

    nine = FIELD_GROUPS["high_impact_oversight"]["columns"]
    assert len(nine) == 9, f"expected nine oversight questions, found {len(nine)}"
    assert FIELD_GROUPS["presumed_not_high_impact"]["columns"] == ["HI_justification"]
