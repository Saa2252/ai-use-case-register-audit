"""The safeguards that travel with the figures onto the application.

The application is a second surface for the same findings, approved by the
owner on 30 September 2026 and recorded in governance/safeguards.md. The rules
that govern the site govern it too, but the site's tests cannot all reach it:
they scan HTML, and this surface is Python that builds its text at run time.

These tests close that distance. A test is never deleted or weakened to make it
pass.

Enforces: S3, S4, S5, S9, S10, S11, S12
"""

import json
import re

from conftest import REPO_ROOT

APP = REPO_ROOT / "app" / "app.py"
DERIVED = REPO_ROOT / "data" / "derived"


def _app_text() -> str:
    return APP.read_text(encoding="utf-8")


# --- S9, S11. One source for the disclaimer and the credit line -------------

def test_the_disclaimer_is_read_and_not_copied():
    """S9. A copy in the page is a second source a correction could miss.

    This is the same failure mode that put four wrong figures on the site, so
    it is checked rather than trusted.
    """
    findings = json.loads((DERIVED / "findings.json").read_text(encoding="utf-8"))
    assert 'findings["disclaimer"]' in _app_text(), (
        "the application must read the disclaimer from data/derived"
    )
    assert findings["disclaimer"] not in _app_text(), (
        "the disclaimer is written out in app/app.py. It must be read, not copied"
    )


def test_the_authorship_line_is_read_and_not_copied():
    """S11."""
    findings = json.loads((DERIVED / "findings.json").read_text(encoding="utf-8"))
    assert findings["authorship"].startswith("Governance design by")
    assert 'findings["authorship"]' in _app_text()
    assert findings["authorship"] not in _app_text()


# --- S3. No comparison between agencies -------------------------------------

def test_the_application_offers_no_agency_filter_or_sort():
    """Owner ruling, 29 September 2026, recorded in decision-rules.md 23.2.

    A page honours S3 by choosing what to publish. An application with a filter
    cannot, because the reader assembles the comparison themselves. This checks
    the controls that could carry one, rather than the word "agency", which the
    page uses legitimately when naming the one entry it works through.
    """
    controls = ["st.selectbox", "st.multiselect", "st.radio", "st.data_editor",
                "st.dataframe", "st.table", "st.slider", "st.select_slider"]
    present = [c for c in controls if c in _app_text()]
    assert not present, (
        "these controls can filter or sort a table of agencies, which the owner "
        "ruled out: " + ", ".join(present)
    )


def test_the_application_never_opens_row_level_data():
    """The second half of the same rule.

    While the application lived in its own repository, the row-level register
    was simply not there to sort. Inside this repository it is, so that
    protection is gone and this test replaces it: the application may read the
    two findings files and nothing else. Recorded as a weakening in
    governance/safeguards.md, because a test is a weaker guard than an absence.
    """
    text = _app_text()
    reads = set(re.findall(r'load\(\s*"([^"]+)"\s*\)', text))
    allowed = {"findings.json", "fieldset.json"}
    assert reads <= allowed, (
        "the application reads files outside the approved set: "
        + ", ".join(sorted(reads - allowed))
    )
    for forbidden in ("register_2025_scrubbed", "oversight_information_pack",
                      "cots_2025_scrubbed", ".csv", "read_csv", "glob("):
        assert forbidden not in text, (
            "app/app.py refers to row-level data: '" + forbidden + "'"
        )


# --- S5. Every figure is read, never typed ----------------------------------

def test_no_figure_is_typed_into_the_application():
    """S5. T5 enforces this for HTML. This is the same rule for the page.

    A number of three or more digits on this page would be a finding, and a
    finding is read from data/derived. Shorter numbers are layout.
    """
    text = _app_text()
    # Theme colours and years are not figures.
    text = re.sub(r"#[0-9a-fA-F]{6}", "", text)
    text = re.sub(r"\b(19|20)\d{2}\b", "", text)
    found = re.findall(r"\b\d{3,}\b", text)
    assert not found, "figures typed into the application: " + ", ".join(sorted(set(found)))


def test_every_figure_the_application_states_resolves():
    """S5, the other half. The keys the page reads exist in the derived files."""
    fieldset = json.loads((DERIVED / "fieldset.json").read_text(encoding="utf-8"))
    for key in ("entries", "high_impact", "no_oversight"):
        assert isinstance(fieldset["lead"][key], int), "lead." + key
    for key in ("fields", "a_real_entry_can_fill", "a_real_entry_cannot_fill",
                "not_collected", "asked_and_left_empty"):
        assert isinstance(fieldset["headline"][key], int), "headline." + key


def test_the_split_the_application_states_closes():
    """The lead states a split of the ten fields. It has to add up."""
    head = json.loads((DERIVED / "fieldset.json").read_text(encoding="utf-8"))["headline"]
    assert head["a_real_entry_can_fill"] + head["a_real_entry_cannot_fill"] == head["fields"]
    assert head["not_collected"] + head["asked_and_left_empty"] == head["a_real_entry_cannot_fill"]


# --- S12. The approved shape of the application -----------------------------

def test_the_application_is_one_page_and_no_more():
    """S12. The scope change approved one page, not a multi-page application."""
    files = sorted(p.name for p in (REPO_ROOT / "app").glob("*.py"))
    assert files == ["app.py"], "files in app/: " + ", ".join(files)
    assert not (REPO_ROOT / "app" / "pages").exists(), (
        "a pages/ directory turns this into a multi-page application, which was "
        "not approved"
    )
