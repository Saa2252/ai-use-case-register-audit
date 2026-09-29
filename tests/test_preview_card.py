"""The social preview card, and the rule it was built to avoid bending.

A card is the only part of this project that travels on its own. Someone sees
it in a feed without the page around it, so what it says has to hold by itself.

Enforces: S5, S9-adjacent. See governance/safeguards.md.
"""

import re

from conftest import REPO_ROOT

from src.disclaimer import SITE_URL

DOCS = REPO_ROOT / "docs"
CARD = DOCS / "assets" / "preview.png"

REQUIRED_TAGS = [
    'property="og:title"',
    'property="og:description"',
    'property="og:url"',
    'property="og:image"',
    'property="og:image:alt"',
    'name="twitter:card"',
]


def test_every_page_carries_the_card_tags():
    """A link to any page should preview, not just the landing page."""
    missing = []
    for path in sorted(DOCS.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        for tag in REQUIRED_TAGS:
            if tag not in text:
                missing.append(path.name + ": " + tag)
    assert not missing, "preview tags missing:\n" + "\n".join(missing)


def test_each_page_points_the_card_at_itself():
    """A card that names the wrong page sends the reader somewhere else."""
    wrong = []
    for path in sorted(DOCS.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        found = re.search(r'property="og:url" content="([^"]+)"', text)
        assert found, path.name + " has no og:url"
        expected = SITE_URL if path.name == "index.html" else SITE_URL + path.name
        if found.group(1) != expected:
            wrong.append(path.name + ": " + found.group(1))
    assert not wrong, "og:url pointing at the wrong page:\n" + "\n".join(wrong)


def test_the_card_description_holds_no_figure():
    """The narrower of the two options, and the reason this test exists.

    A card's text is static, because the crawler reading it does not run
    scripts. Putting a figure there would mean a literal number in the page
    head, and widening T5 from "no digits in published HTML" to "no digits
    except the ones the build wrote". The figure is in the card image instead,
    drawn from data/derived. This checks the description stays free of them, so
    the decision cannot drift.
    """
    offenders = []
    for path in sorted(DOCS.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        for found in re.finditer(r'(?:name="description"|property="og:description") '
                                 r'content="([^"]*)"', text):
            for digits in re.finditer(r"\d", found.group(1)):
                offenders.append(path.name + ": '" + found.group(1)[:60] + "'")
                break
    assert not offenders, (
        "a figure in the card description. It belongs in the card image:\n"
        + "\n".join(offenders)
    )


def test_the_card_image_exists_and_is_the_expected_shape():
    """A card of the wrong size is cropped by the platform, not rejected."""
    assert CARD.exists(), "docs/assets/preview.png is missing. Run scripts/build_preview.py"
    header = CARD.read_bytes()[:24]
    assert header[:8] == b"\x89PNG\r\n\x1a\n", "the card is not a PNG"
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    assert (width, height) == (1200, 630), f"card is {width}x{height}, expected 1200x630"


def test_the_card_figure_is_current():
    """The card holds a figure drawn at build time. It can go stale.

    The image cannot be read back for its number without an image library the
    site does not otherwise need, so this checks the weaker thing that still
    catches the real failure: the card is not older than the data it draws from.
    """
    import json

    source = REPO_ROOT / "data" / "derived" / "fieldset.json"
    assert source.exists()
    json.loads(source.read_text(encoding="utf-8"))
    assert CARD.stat().st_mtime >= source.stat().st_mtime, (
        "the card is older than the figures it draws from. "
        "Run scripts/build_preview.py"
    )
