"""The fifth page answers the five gaps the fourth page names, and no more.

The owner scoped this page to exactly the five things the field set page says
it does not do. The risk in a page like this is not that it is wrong. It is
that it quietly turns into a governance framework, answering things nobody
asked and burying the five it was written for.

Four checks hold the scope.

1. The two pages name the same five gaps. They read one list, and this proves
   the published files agree rather than trusting that they do.
2. Every gap has a mechanism and every mechanism answers a gap.
3. Every mechanism answers the same five questions, all of them filled in. A
   mechanism that answers four is a paragraph wearing the shape of a design.
4. Every mechanism states a cost. A proposal with no costs in it is a wish, and
   the cost line is the one that goes missing first.

Verified by planting the failure: emptying any mechanism's cost fails check 4
and names it, and adding a sixth mechanism fails check 2.
"""

import json
import sys

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src.fieldset import OPERATING_GAPS  # noqa: E402

DOCS_DATA = REPO_ROOT / "docs" / "data"

# The five answers every mechanism gives, in the order the page prints them.
ANSWERS = ["mechanism", "who", "trigger", "record", "cost"]


def _page() -> dict:
    return json.loads((DOCS_DATA / "operating_model.json").read_text(encoding="utf-8"))


def _field_set() -> dict:
    return json.loads((DOCS_DATA / "fieldset.json").read_text(encoding="utf-8"))


def test_both_pages_name_the_same_gaps():
    named_on_the_field_set = [g["name"] for g in _field_set()["not_covered"]["missing"]]
    answered_here = [m["name"] for m in _page()["mechanisms"]]
    assert named_on_the_field_set == answered_here, (
        "the page naming the gaps and the page answering them disagree:\n"
        f"  field set: {named_on_the_field_set}\n"
        f"  this page: {answered_here}"
    )


def test_every_gap_has_a_mechanism_and_every_mechanism_has_a_gap():
    gaps = {g["key"] for g in OPERATING_GAPS}
    mechanisms = {m["key"] for m in _page()["mechanisms"]}
    assert gaps == mechanisms, (
        "the scope the owner set was these five gaps and nothing else.\n"
        f"  gaps with no mechanism: {sorted(gaps - mechanisms)}\n"
        f"  mechanisms answering no gap: {sorted(mechanisms - gaps)}"
    )


def test_every_mechanism_answers_the_same_five_questions():
    thin = []
    for m in _page()["mechanisms"]:
        for answer in ANSWERS:
            if not str(m.get(answer, "")).strip():
                thin.append(f"{m['key']} does not say: {answer}")
    assert not thin, (
        "a mechanism does not answer what the others answer, so it cannot be read "
        "against them:\n" + "\n".join(thin)
    )


def test_every_mechanism_states_what_it_costs():
    """The line that goes missing first, checked on its own for that reason."""
    free = [m["key"] for m in _page()["mechanisms"] if not str(m.get("cost", "")).strip()]
    assert not free, (
        "a mechanism is proposed with no cost stated: " + ", ".join(sorted(free))
    )


def test_the_page_says_it_has_not_been_tested():
    status = _page()["status"]
    for key in ("label", "what_this_is", "what_this_is_not", "why_it_is_separate", "scope"):
        assert str(status.get(key, "")).strip(), f"the standing note has no {key}"
    assert "not been used" in status["what_this_is_not"], (
        "the standing note no longer says the proposal has not been used to keep a register"
    )


def test_the_page_says_what_would_show_it_wrong():
    wrong = _page()["would_show_it_wrong"]
    assert len(wrong) >= 3, (
        "a design with no way of being wrong is not a design, and this page lists "
        f"{len(wrong)} ways"
    )
