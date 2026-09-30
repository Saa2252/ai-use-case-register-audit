"""Every published share is divided by the entries the question was put to.

This project published a figure counting blanks in the nine oversight fields
across all 445 entries marked high-impact. The publisher's dictionary requires
those nine "only for high-impact deployed use cases", and 218 of the 445 are
not deployed. The register never put the question to them, so their blanks were
not unanswered questions. The figure was corrected from 317 of 445 to 101 of
227.

The correction was made by hand, on that one measure. Nothing checked the rest.
Twenty-two of this register's thirty-three fields carry a condition, and every
share of them was being divided by all 3,611 rows. The date field was the most
visible: usable dates read as a third of the register and are two thirds of the
entries the register asks for a date.

Three checks hold the correction in place.

1. Every field's Required clause can still be read. A clause the parser has not
   been taught raises rather than defaulting to "asked of every entry", because
   that default is what produced the defect.
2. For every conditional field, both views are published, and the population
   the question is put to is smaller than the register.
3. The figures the site puts in front of a reader for the date field come from
   the population the register asks, not from every row.

Verified by planting the failure: pointing the evidence strip back at
`usable_dates_as_share_of_all_rows` fails the third check by name, and adding an
unreadable Required clause to the dictionary fails the first.
"""

import json
import sys

import pytest

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src import conditionality as COND  # noqa: E402
from src.fieldset import EVIDENCE  # noqa: E402

DERIVED = REPO_ROOT / "data" / "derived"
REGISTER = DERIVED / "register_2025_scrubbed.csv"


def _findings() -> dict:
    payload = json.loads((DERIVED / "findings.json").read_text(encoding="utf-8"))
    return {f["measure"]: f for f in payload["findings"]}


def test_every_required_clause_can_still_be_read():
    if not COND.DICTIONARY.exists():
        pytest.skip("raw data not present: run the acquisition step first")
    dictionary = COND._dictionary()
    unreadable = []
    for field in dictionary:
        try:
            COND.condition(field, dictionary)
        except ValueError as problem:
            unreadable.append(str(problem))
    assert not unreadable, (
        "a Required clause changed and the analysis can no longer tell which entries "
        "the register asks:\n" + "\n".join(unreadable)
    )


def test_a_conditional_field_is_never_published_only_over_every_row():
    m2 = _findings()["M2"]
    where = m2["field_completeness_where_asked"]
    rows = m2["rows"]
    missing = [f for f in m2["field_completeness_all_rows"] if f not in where]
    assert not missing, (
        "a field is published as a share of all rows with no figure for the entries "
        "it is asked of: " + ", ".join(sorted(missing))
    )
    not_narrowed = [f for f, v in where.items()
                    if v["conditional"] and v["asked_of"] >= rows]
    assert not not_narrowed, (
        "a field the dictionary marks conditional is still counted against every row: "
        + ", ".join(sorted(not_narrowed))
    )


def test_the_conditional_shares_actually_differ_from_the_all_row_shares():
    """If they matched, the condition was not applied."""
    m2 = _findings()["M2"]
    all_rows = m2["field_completeness_all_rows"]
    where = m2["field_completeness_where_asked"]
    same = [f for f, v in where.items()
            if v["conditional"] and v["share"] == all_rows.get(f)]
    assert not same, (
        "a conditional field reports the same share both ways, so the condition was "
        "not applied to it: " + ", ".join(sorted(same))
    )


def test_the_date_figures_the_site_shows_come_from_the_entries_it_asks():
    m3 = _findings()["M3"]
    assert "operational_date_where_asked" in m3, (
        "M3 no longer carries the date figures measured against the entries the "
        "register asks for a date"
    )
    block = m3["operational_date_where_asked"]
    assert block["entries_asked"] < m3["operational_date"]["rows_with_a_value"] + block["entries_not_asked"], (
        "the asked population is not narrower than the register"
    )
    on_strip = [item["path"] for item in EVIDENCE if "operational_date" in item["path"]]
    assert on_strip == ["M3.operational_date_where_asked.usable_dates_as_share_of_entries_asked"], (
        "the landing page evidence strip shows a date share that is not measured "
        f"against the entries the register asks: {on_strip}"
    )


def test_entries_that_cannot_be_placed_are_reported_and_not_folded_in():
    """338 entries record no stage. A condition written in terms of stage cannot
    place them, and a count that puts them on either side asserts something the
    file does not hold."""
    m3 = _findings()["M3"]["operational_date_where_asked"]
    assert m3["entries_undetermined"] > 0, "the undetermined group is no longer reported"
    total = m3["entries_asked"] + m3["entries_not_asked"] + m3["entries_undetermined"]
    assert total == _findings()["M2"]["rows"], (
        f"the three groups sum to {total} and the register holds "
        f"{_findings()['M2']['rows']} entries"
    )


def test_a_prominent_correction_is_actually_on_the_pages_it_names():
    """A correction that stays in the file is not a correction.

    The wrong figure was read on a public page. The note saying it changed
    belongs on that page, and this checks it arrived there rather than only in
    the JSON.
    """
    docs = REPO_ROOT / "docs"
    payload = json.loads((DERIVED / "findings.json").read_text(encoding="utf-8"))
    corrections = payload["corrections"]
    assert corrections, "the findings carry no corrections"
    missing = []
    for name, item in corrections.items():
        for page in item["pages"]:
            text = (docs / page).read_text(encoding="utf-8")
            if f'data-figure="corrections.{name}.text"' not in text:
                missing.append(f"{page} does not carry the correction '{name}'")
    assert not missing, "\n".join(missing)


def test_the_correction_log_records_every_published_correction():
    log = (REPO_ROOT / "governance" / "corrections.md").read_text(encoding="utf-8")
    payload = json.loads((DERIVED / "findings.json").read_text(encoding="utf-8"))
    for name, item in payload["corrections"].items():
        assert item["date"] in log, (
            f"correction '{name}' is published and its date {item['date']} is not in "
            "governance/corrections.md"
        )


def test_every_oversight_figure_is_based_on_the_entries_the_register_asks():
    """The same fault, found three times, now checked rather than remembered.

    First the headline count of blanks was divided by 445. That was corrected
    by hand. Then every conditional field's completeness was found to have the
    same shape, and a rule was written for it. Neither pass looked at the
    per-question coverage table or at the reading of what the answers say, and
    both were still divided by 445 until 30 September 2026.

    Each correction fixed the figure in front of it. This checks the class.

    Anything in M4 measured across every flagged entry carries `_all_flagged`
    in its name and is published beside the narrower figure, never instead of
    it. Anything without that suffix is measured against the 227.
    """
    m4 = _findings()["M4"]
    asked = m4["asked_the_nine"]
    flagged = m4["subset_size"]
    assert asked < flagged, (
        "the entries the register asks the nine of are no longer a subset of the "
        "entries flagged high-impact, which is the premise of the whole correction")

    answers = m4["oversight_answers"]
    assert answers["entries"] == asked, (
        f"the reading of the answers covers {answers['entries']} entries and the register "
        f"asks {asked}")
    assert answers["possible_answers"] == asked * answers["fields"], (
        "the number of places an answer could sit is not the asked entries times the "
        "nine fields")

    wider = m4["oversight_answers_all_flagged"]
    assert wider["entries"] == flagged, (
        "the wider reading is no longer the wider reading")
    for block in (answers, wider):
        assert block["population"].strip(), (
            "a reading of the answers does not name the entries it read")


def test_the_per_question_coverage_is_published_both_ways_and_they_differ():
    m4 = _findings()["M4"]
    narrow = m4["oversight_field_coverage"]
    wide = m4["oversight_field_coverage_all_flagged"]
    assert set(narrow) == set(wide), "the two coverage tables cover different questions"
    same = [k for k in narrow if narrow[k] == wide[k]]
    assert not same, (
        "a question reports the same share against both populations, so the condition "
        "was not applied to it: " + ", ".join(sorted(same))
    )
    for key in ("primary", "secondary"):
        assert m4["coverage_bases"][key].strip(), f"the coverage table does not name its {key} base"


def test_the_page_states_both_halves_of_the_condition():
    """Half a condition above a table is how every share below it went wrong."""
    labels = json.loads((REPO_ROOT / "docs" / "data" / "field_labels.json")
                        .read_text(encoding="utf-8"))
    groups = {v for k, v in labels["group_of"].items() if k.startswith("hi_")}
    assert groups, "the nine oversight fields no longer carry a group label"
    for group in groups:
        lowered = group.lower()
        assert "high-impact" in lowered and "deployed" in lowered, (
            "the group label above the per-question table states only part of the "
            f"condition: {group!r}")
