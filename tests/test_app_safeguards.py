"""The Streamlit application serves the site and restates nothing.

The first version of this application rebuilt the project's findings in
Streamlit components, and the owner dropped it the next day because it could
not reproduce the page as a designed object. The reasoning is in
governance/decision-rules.md section 23.5.

This version does not rebuild anything. It removes Streamlit's own interface
and serves the published site in a frame, so the design is not approximated
because it is not reproduced.

That shape is the safeguard. An application holding no figure cannot publish a
figure wrongly, and this project has corrected the same kind of figure three
times. These checks hold the shape rather than trusting it.

1. It restates no finding: it reads no data file and imports nothing from the
   analysis.
2. The address it serves and the disclaimer it falls back to come from
   src/disclaimer.py, so it cannot state either differently from the site.
3. The ground it paints behind the frame is the site's own, in both schemes,
   read out of the stylesheet rather than trusted.
4. The published site's address is stated once and the README agrees with it.

Verified by planting the failure: adding a figure, a data-file read, or an
import from src.measures each fails a check by name, and changing either
ground colour fails the third.
"""

import re
import sys

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src.disclaimer import SITE_URL  # noqa: E402

APP = REPO_ROOT / "app" / "app.py"
STYLESHEET = REPO_ROOT / "docs" / "assets" / "style.css"
README = REPO_ROOT / "README.md"


def _app() -> str:
    assert APP.exists(), "the application is gone; remove this file with it"
    return APP.read_text(encoding="utf-8")


def test_the_application_reads_no_data_and_restates_no_finding():
    """The absence of the data is a stronger guard than any test of the output.

    Section 23.4 recorded that losing this absence was the real cost of the
    first version. This version gets it back: there is no data in it to
    restate.
    """
    text = _app()
    forbidden = [
        "data/derived", "findings.json", "fieldset.json", "register_table",
        "reusability_findings", "operating_model.json", "read_csv", "read_json",
        "from src.measures", "from src import measures", "import pandas",
    ]
    found = [f for f in forbidden if f in text]
    assert not found, (
        "the application reaches data it should not hold. It serves the published site "
        "and restates nothing:\n  " + "\n  ".join(found)
    )


def test_the_application_states_no_figure():
    """A number here would be a second copy of a finding, which is the failure
    this project has had repeatedly. The only numbers allowed are CSS lengths
    and the height the frame is born with."""
    text = _app()
    # Strip the stylesheet block and the documented iframe height, which are
    # layout rather than findings.
    without_css = re.sub(r"<style>.*?</style>", "", text, flags=re.S)
    without_css = without_css.replace("height=900", "")
    numbers = re.findall(r"\b\d{3,}\b", without_css)
    assert not numbers, (
        "the application states a figure of its own: " + ", ".join(sorted(set(numbers)))
    )


def test_the_address_and_the_disclaimer_come_from_one_place():
    text = _app()
    assert "from src.disclaimer import" in text, (
        "the application no longer imports its address and disclaimer from the one place "
        "that holds them")
    for name in ("SITE_URL", "DISCLAIMER", "AUTHORSHIP"):
        assert name in text, f"the application no longer uses {name}"
    typed = re.findall(r'"https://[^"]+"', text)
    assert not typed, (
        "the application types an address instead of importing it: " + ", ".join(typed)
    )


def test_the_ground_behind_the_frame_is_the_sites_own():
    """Streamlit paints its own background and cannot follow the system scheme.

    The application sets it instead, in a media query, so the moment before the
    site appears looks like the site. These two values are the site's own, and
    this reads them out of the stylesheet rather than trusting that they match.
    """
    css = STYLESHEET.read_text(encoding="utf-8")
    light = re.search(r":root\s*\{[^}]*?--bg:\s*(#[0-9a-fA-F]{3,8})", css, re.S)
    dark = re.search(r"@media \(prefers-color-scheme: dark\).*?--bg:\s*(#[0-9a-fA-F]{3,8})",
                     css, re.S)
    assert light and dark, "the stylesheet no longer declares a --bg in both schemes"
    text = _app().lower()
    for scheme, found in (("light", light), ("dark", dark)):
        value = found.group(1).lower()
        assert value in text, (
            f"the {scheme} ground behind the frame is not the site's {value}. The window "
            "would flash a colour the site never uses while the frame loads."
        )


def test_the_site_address_is_stated_once():
    readme = README.read_text(encoding="utf-8")
    assert SITE_URL.rstrip("/") in readme, (
        "the README states a different address for the site than src/disclaimer.py does")
