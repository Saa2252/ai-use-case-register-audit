"""Figures this project published and later changed, and where each one ran.

A correction that only reaches the file is not a correction. The wrong number
was on a public page and was read there, so the note saying it was wrong goes
on the same page, near the top, for as long as the owner decides.

Each entry carries a template rather than a finished sentence. The numbers in
it are resolved from the published findings at build time, like every other
number on this site, so a correction cannot itself go stale (S5). The owner
approves the wording; the figures are computed.

`prominent` is a governance decision, not a clock. A note stops being
prominent when the owner says so, and the record in governance/corrections.md
is permanent either way.
"""

from __future__ import annotations

CORRECTIONS = [
    {
        "id": "oversight_denominator",
        "date": "2026-09-30",
        "prominent": True,
        "pages": ["index.html", "register.html"],
        "heading": "Correction, 2026-09-30",
        "template": (
            "An earlier version of this site counted the nine oversight questions across "
            "all {flagged} entries marked high-impact and reported {flagged_none} with none "
            "answered. The register's own dictionary asks those nine only of high-impact "
            "entries that are deployed. Counted against the {asked} entries it does ask, the "
            "figure is {asked_none}, or {share}%. The gap is smaller and it is still there. "
            "Every other field's denominator was then checked against the dictionary. The "
            "same fault was found in the one date field and corrected with it. The check is "
            "recorded in governance/corrections.md."
        ),
        "figures": {
            "flagged": "M4.subset_size",
            "flagged_none": "M4.oversight_block_shape.none_answered",
            "asked": "M4.oversight_conditionality.required_of.entries",
            "asked_none": "M4.oversight_conditionality.required_of.none_answered",
            "share": "M4.oversight_conditionality.required_of.share_none_answered",
        },
    },
    {
        "id": "oversight_base",
        "date": "2026-09-30",
        "prominent": True,
        "pages": ["obligations.html"],
        "heading": "Correction, 2026-09-30",
        "template": (
            "Every per-question figure on this page, and the reading of what the answers "
            "say, was divided by all {flagged} entries flagged high-impact. The register "
            "asks these nine only of the {asked} that are also deployed. Measured against "
            "those, the share of answers saying a step is under way is {in_progress}% rather "
            "than {in_progress_before}%, the share saying a step was done is {done}% rather "
            "than {done_before}%, and each question is answered on about {coverage}% of "
            "entries rather than about {coverage_before}%. The picture is less empty than "
            "this page showed. This is the third figure on this site corrected for the same "
            "reason, and the check that now covers the class is in "
            "governance/corrections.md."
        ),
        "figures": {
            "flagged": "M4.subset_size",
            "asked": "M4.asked_the_nine",
            "in_progress": "M4.oversight_answers.share.in progress",
            "in_progress_before": "M4.oversight_answers_all_flagged.share.in progress",
            "done": "M4.oversight_answers.share.done",
            "done_before": "M4.oversight_answers_all_flagged.share.done",
            "coverage": "M4.oversight_field_coverage.hi_testing_conducted",
            "coverage_before": "M4.oversight_field_coverage_all_flagged.hi_testing_conducted",
        },
    },
    {
        "id": "date_denominator",
        "date": "2026-09-30",
        # Not prominent: this figure sits inside a section on the gaps page and
        # the correction is printed there, beside it, rather than at the top of
        # a page most of its readers arrive at for something else.
        "prominent": False,
        "pages": ["gaps.html"],
        "heading": "Correction, 2026-09-30",
        "template": (
            "The one date field was reported as a share of every row in the register. The "
            "dictionary asks for it only of entries at the pilot and deployed stages. "
            "Usable dates were published as {all_rows}% of the register and are {asked}% of "
            "the {asked_entries} entries the register asks."
        ),
        "figures": {
            "all_rows": "M3.operational_date.usable_dates_as_share_of_all_rows",
            "asked": "M3.operational_date_where_asked.usable_dates_as_share_of_entries_asked",
            "asked_entries": "M3.operational_date_where_asked.entries_asked",
        },
    },
]


def resolve(resolver) -> dict:
    """Build each correction's finished text. `resolver` takes a figure path.

    Raises if a figure a correction names is not in the findings, because a
    correction with a missing number would publish a sentence with a hole in
    it where the number that was wrong should be.
    """
    out = {}
    for item in CORRECTIONS:
        values = {}
        for name, path in item["figures"].items():
            value = resolver(path)
            if value is None:
                raise SystemExit(
                    f"correction {item['id']}: the findings carry nothing at {path}")
            values[name] = value
        out[item["id"]] = {
            "date": item["date"],
            "heading": item["heading"],
            "prominent": item["prominent"],
            "pages": item["pages"],
            "text": item["template"].format(**values),
        }
    return out
