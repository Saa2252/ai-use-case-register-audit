"""The picture a link to this site shows when it is pasted somewhere else.

A preview card is the one piece of this project that travels with none of its
context. It arrives in a feed with no selection rule beside it, no caveat under
it, and no page around it. Two rules follow from that, and both are checked.

**It names no organisation.** The worked panel on the site names the entry and
the agency, which S3 permits as published facts in row-level detail. A card is
not row-level detail. It is a picture that arrives alone, and a published fact
shown alone is read as a point being made.

**Its figures cannot drift from the data.** This project has published a wrong
figure four times. A picture is the worst place for a fifth, because nothing on
it can be re-read from the file by a reader. So the card is drawn from the
findings by a script, and the figures it was drawn from are recorded beside it
and compared here.

Verified by planting the failure: changing any figure in the stamp fails the
staleness check by name, and making the card script read an agency column fails
the naming check. Both columns are covered, so a row that stops being answered
on either side shows up here rather than on the card.
"""

import json
import re
import sys

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src.disclaimer import SITE_URL  # noqa: E402

DOCS = REPO_ROOT / "docs"
CARD = DOCS / "assets" / "card.png"
STAMP = DOCS / "assets" / "card.stamp"
SCRIPT = REPO_ROOT / "scripts" / "build_card.py"

REQUIRED_TAGS = ["og:title", "og:description", "og:url", "og:image", "twitter:card"]


def _tags(page) -> dict:
    text = page.read_text(encoding="utf-8")
    return dict(re.findall(r'<meta property="([^"]+)" content="([^"]*)">', text))


def test_every_page_carries_a_preview():
    missing = []
    for page in sorted(DOCS.glob("*.html")):
        tags = _tags(page)
        for name in REQUIRED_TAGS:
            if not tags.get(name, "").strip():
                missing.append(f"{page.name}: {name}")
    assert not missing, (
        "a page would paste into a feed with no preview, or a broken one:\n"
        + "\n".join(missing)
    )


def test_the_preview_points_at_the_published_card_by_absolute_address():
    """A relative address here resolves against the host reading the page.

    The scraper is on another machine. A relative og:image would send it to
    that machine's own assets directory, which is why these are absolute and
    why they needed an exemption.
    """
    expected = SITE_URL + "assets/card.png"
    wrong = []
    for page in sorted(DOCS.glob("*.html")):
        tags = _tags(page)
        if tags.get("og:image") != expected:
            wrong.append(f"{page.name}: og:image is {tags.get('og:image')}")
        if not tags.get("og:url", "").startswith(SITE_URL):
            wrong.append(f"{page.name}: og:url is {tags.get('og:url')}")
    assert not wrong, "a preview points somewhere other than the published card:\n" + "\n".join(wrong)


def test_the_card_exists_and_is_the_size_the_hosts_crop_to():
    """Read out of the picture, not out of a number declared next to it.

    The hosts show a large card at 1200x627 and drop to a thumbnail below that, so the size is part of whether this works at all.
    """
    from PIL import Image

    assert CARD.exists(), "the card image is gone"
    with Image.open(CARD) as image:
        assert image.size == (1200, 627), (
            f"the card is {image.size[0]}x{image.size[1]} and the hosts crop to 1200x627, "
            "so it would be cut or shown as a thumbnail")


def test_the_card_has_not_drifted_from_the_findings():
    """A wrong number in a picture is the worst kind, because a reader cannot
    re-read it from the file."""
    assert STAMP.exists(), "the card carries no record of what it was drawn from"
    drawn = json.loads(STAMP.read_text(encoding="utf-8"))
    payload = json.loads((DOCS / "data" / "fieldset.json").read_text(encoding="utf-8"))
    head = payload["headline"]
    now = {
        "fields": head["fields"],
        "answered": head["a_real_entry_can_fill"],
        "not_collected": head["not_collected"],
        "asked_and_left_empty": head["asked_and_left_empty"],
        "does_not_apply": head["does_not_apply"],
        "meeting_the_rule": head["entries_meeting_the_rule"],
        "states": [row["state"] for row in payload["panel_one"]["rows"]],
        "made_up": [row["state"] for row in payload["panel_two"]["rows"]],
    }
    stale = [k for k, v in now.items() if drawn.get(k) != v]
    assert not stale, (
        "the card was drawn from figures the findings no longer hold: "
        + ", ".join(sorted(stale))
        + "\nRun: python scripts/build_card.py"
    )


def test_the_card_names_no_organisation():
    """It cannot name one, because it never reads the columns that hold names."""
    source = SCRIPT.read_text(encoding="utf-8")
    forbidden = ["agency", "agency_name", "use_case_name", "entry_id", "panel_one\"][\"rows\"][0]"]
    found = [f for f in forbidden if f in source.replace("# ", "").split('"""')[-1]]
    assert not found, (
        "the card script reaches a column that holds a name. A card travels with "
        "none of the page around it, so a name on it arrives with no selection "
        "rule and no caveat beside it: " + ", ".join(found)
    )
    drawn = json.loads(STAMP.read_text(encoding="utf-8"))
    assert not any(isinstance(v, str) and len(v) > 40 for v in drawn.values()), (
        "the card stamp carries free text, which is where a name would be")
