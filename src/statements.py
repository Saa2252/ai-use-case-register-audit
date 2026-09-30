"""Facts this site states on more than one page, held in one place.

A fact written out independently on two pages is two facts that can disagree.
This project has already been bitten twice: an emptiness rule implemented in two
places had drifted before anyone looked, and a sentence about who has to publish
a register was corrected on one page and survived unchanged on another.

Each statement below is substituted into the page bodies by
scripts/build_site.py wherever `{{key}}` appears. A page never writes one of
these out. tests/test_single_source_statements.py fails if one does.

The wording of a statement is owner-approved copy. Changing it changes every
page at once, which is the point.
"""

from src.measures import FILLED_FIELD, NEVER_SUM

STATEMENTS = {
    # Corrected 30 September 2026. The earlier wording, "Federal agencies in the
    # United States have to publish a list", asserted a duty whose scope this
    # project cannot verify from the data. The governing memorandum is named in
    # governance/data-provenance.md.
    "publication_duty":
        "US federal agencies publish a list of the AI systems they use once a "
        "year, under a White House policy memorandum.",

    # The publisher's own definition, not a gloss. governance/decision-rules.md
    # section 19 records which plain-English glosses are the author's.
    "high_impact_meaning":
        "the agency judged the system's output to be the principal basis for a "
        "decision affecting people",

    # Already single-sourced in src.measures and used by the findings. The
    # register page used to write it out again by hand.
    "filled_field": FILLED_FIELD,

    "reached_the_file":
        "The pattern describes what reached the file, not the oversight "
        "practice itself.",

    # What this project read. Held here because the field set page stated it
    # twice in its own words, and both copies still said two registers after
    # the comparator changed on 30 September 2026. A sentence that names the
    # sources cannot be wrong about how many there are.
    "sources_read":
        "This project read the US federal list in full, and compares what a "
        "register asks against the United Kingdom's recording standard, which "
        "publishes a field template rather than entries.",

    "never_summed": NEVER_SUM,
}


def apply(text: str) -> str:
    """Replace every `{{key}}` token with its statement."""
    for key, value in STATEMENTS.items():
        text = text.replace("{{" + key + "}}", value)
    return text
