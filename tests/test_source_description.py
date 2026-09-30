"""How the site describes the sources it read, checked against what it read.

The comparator changed on 30 September 2026 from the Government of Ontario's
list to the United Kingdom's recording standard. Every field card, the gaps
table and the sources table were changed with it. Two sentences on the field
set page were not, and both still said the project had read two registers and
named Ontario as the second. Nothing caught them, because no test reads copy
about the sources.

A page whose argument is provenance cannot describe its own sources wrongly.
Two checks hold that.

1. No published copy counts the sources. A count goes stale the moment a source
   changes, and the count is what went stale here. Copy names the sources
   instead, and a name that is wrong is visible to a reader in a way a number
   is not.
2. Every proposed field states what the current comparator asks, and none
   carries a leftover key for the previous one.

Verified by planting the failure: restoring either original sentence to
`scripts/bodies/view4.html` makes the first check fail and names the file and
the phrase, and renaming a field's `uk` key to `ontario` makes the second fail
and names the field.
"""

import json
import sys

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src.fieldset import EMPTY_CONVENTION, FIELDS  # noqa: E402

BODIES = REPO_ROOT / "scripts" / "bodies"
DOCS = REPO_ROOT / "docs"

# Forms of words that state how many sources were read rather than naming them.
# Each one was either in the published copy or one edit away from it.
#
# "two published files" is deliberately not here. The gaps page uses it about
# the two near-identical files in the 2024 repository, which is a different and
# true statement, and a check that fails on a true sentence teaches people to
# work around it.
COUNTING_FORMS = [
    "two registers",
    "both registers",
    "either register",
    "two published registers",
    "the two registers",
    "two real registers",
    "three registers",
]

# The comparator's key on every proposed field, and the key it replaced.
COMPARATOR = "uk"
FORMER_COMPARATOR = "ontario"


def _normalise(text: str) -> str:
    return " ".join(text.replace("’", "'").split()).lower()


def test_no_published_copy_counts_the_sources():
    found = []
    for path in sorted(BODIES.glob("*.html")) + sorted(DOCS.glob("*.html")):
        text = _normalise(path.read_text(encoding="utf-8"))
        for phrase in COUNTING_FORMS:
            if phrase in text:
                found.append(f"{path.name} says '{phrase}'")
    assert not found, (
        "published copy counts the sources instead of naming them, which is how "
        "the comparator change was missed:\n" + "\n".join(found)
    )


def test_every_proposed_field_states_what_the_comparator_asks():
    missing = []
    leftover = []
    for item in list(FIELDS) + [EMPTY_CONVENTION]:
        if not item.get(COMPARATOR, "").strip():
            missing.append(item["name"])
        if FORMER_COMPARATOR in item:
            leftover.append(item["name"])
    assert not missing, (
        "a proposed field does not say what the comparator asks: " + ", ".join(missing)
    )
    assert not leftover, (
        "a proposed field still carries the previous comparator: " + ", ".join(leftover)
    )


def test_the_published_field_set_carries_the_same_comparator():
    """The built file, not only the source that builds it."""
    payload = json.loads((DOCS / "data" / "fieldset.json").read_text(encoding="utf-8"))
    wrong = [f["name"] for f in payload["fields"]
             if not str(f.get(COMPARATOR, "")).strip() or FORMER_COMPARATOR in f]
    assert not wrong, (
        "the published field set does not carry the comparator on: " + ", ".join(wrong)
    )
