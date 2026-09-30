"""The rules that apply to every figure on this site, written down once.

Five sentences were being repeated across the pages. Two of them appeared on
three pages each. A reader who meets the same qualification four times stops
reading qualifications, which is the opposite of what they are for, and a site
that hedges every number reads as though it does not trust any of them.

So the standing rules live here and are published once, on the landing page,
under a heading a reader can be sent back to. What stays beside a finding is
the one thing that qualifies that finding and nothing else.

This is not a reduction in what the site discloses. Every rule below was
already published; it was published five times over. Moving them here makes
them findable, which repeating them did not.

`applies_to` is for the reader, not the machine: it says where the rule bites,
so somebody can check it against the figure in front of them.
"""

from __future__ import annotations

from src.measures import FILLED_FIELD

HEADING = "How to read these numbers"

LEAD = ("Everything on this site is counted from one published file. These five rules "
        "apply to every figure on every page, so they are stated here once rather than "
        "repeated under each one. A finding carries only what qualifies that finding.")

READING_RULES = [
    {
        # The sentence itself still lives in src/measures.py, where the findings
        # were written against it. This is now the only place it is published.
        "rule": FILLED_FIELD,
        "applies_to": "Every completeness figure, and the nine oversight fields in particular.",
    },
    {
        "rule": "Every figure describes what reached the file, not what any organisation did.",
        "applies_to": "Every figure. This project reads a published file from outside and has "
                      "no access to how any organisation works.",
    },
    {
        "rule": "A share is divided by the entries the register asks, which is often fewer "
                "than the whole file. Where the two differ, both are published and the "
                "narrower one is the one describing a question with no answer.",
        "applies_to": "22 of the register's 31 fields, which are required only under a "
                      "stated condition.",
    },
    {
        "rule": "A published list can only show what was declared. Nothing here says anything "
                "about systems nobody wrote down.",
        "applies_to": "Every count of entries. Undeclared systems are outside anything this "
                      "project can see.",
    },
    {
        "rule": "Nothing here compares one organisation with another, and no entry shown was "
                "picked out. Where a single entry appears, the rule that selected it is "
                "printed beside it.",
        "applies_to": "Every page. There is no ranking, score or league table anywhere on "
                      "this site, and that is a deliberate choice with a cost.",
    },
]

# What a page says instead of repeating the rules. Held here so the four pages
# that point back to the box cannot word it four different ways.
POINTER = "Five rules apply to every figure on this site."
POINTER_LINK_TEXT = "How to read these numbers"
POINTER_HREF = "index.html#how-to-read"
