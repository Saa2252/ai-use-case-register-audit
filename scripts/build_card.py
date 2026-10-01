"""Build the link preview card as a PNG, at the size the host crops to.

A card is the one piece of this project that travels with none of its context.
A reader meets it in a feed, without the selection rule beside it, without the
caveat under it, and without the page it came from. Two things follow.

**No organisation is named on it.** The worked panel on the site names the
entry and the agency, which S3 permits as published facts in row-level detail.
A card is not row-level detail. It is a picture that arrives alone, and a
published fact shown alone is read as a point being made. The owner reached the
same conclusion and blurred both before asking for this.

**Every figure and every box on it is read from the published data**, so the
card cannot show something the audit does not. The ten boxes are the ten rows
of the worked panel, in order, each drawn by its own state: filled for a box
the published entry answers, a solid outline for one the register asks and the
entry leaves empty, dashed for one the register does not collect, and struck
through for one it does not put to an entry like this.

Drawn here rather than captured from a browser. A capture would have been a
manual step producing a picture that nothing could check, and this project has
been caught four times by a published figure that had drifted from its data.
A script that redraws it from the findings cannot drift from them.

Run:  python scripts/build_card.py
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

DOCS = REPO_ROOT / "docs"
ASSETS = DOCS / "assets"

# What the host crops to. Anything outside this is not seen.
WIDTH, HEIGHT = 1200, 627

# The site's own dark tokens. The card is drawn in one scheme because a picture
# cannot follow the reader's, and dark is the one the owner sent.
BG = (20, 21, 15)
INK = (236, 234, 223)
INK_SOFT = (168, 164, 152)
PUB = (143, 196, 174)
ACCENT = (185, 166, 230)
BORDER = (58, 59, 51)

# Font files are looked up rather than assumed, and the one used is recorded in
# the stamp, so a card drawn on another machine can be told from this one.
FONT_CANDIDATES = [
    ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
     "/System/Library/Fonts/Supplemental/Arial.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
]


def fonts():
    for bold, regular in FONT_CANDIDATES:
        if Path(bold).exists() and Path(regular).exists():
            return bold, regular
    raise SystemExit(
        "no font file found for the card. Add this machine's paths to "
        "FONT_CANDIDATES rather than letting it drop to a bitmap font, "
        "which would publish a picture that does not look like the site.")


def figures() -> dict:
    payload = json.loads((DOCS / "data" / "fieldset.json").read_text(encoding="utf-8"))
    head = payload["headline"]
    return {
        "fields": head["fields"],
        "answered": head["a_real_entry_can_fill"],
        "not_collected": head["not_collected"],
        "asked_and_left_empty": head["asked_and_left_empty"],
        "does_not_apply": head["does_not_apply"],
        "meeting_the_rule": head["entries_meeting_the_rule"],
        "states": [row["state"] for row in payload["panel_one"]["rows"]],
    }


def dashed_rect(draw, box, colour, width=3, dash=9, gap=7):
    """Pillow has no dashed stroke, so the four sides are drawn in pieces."""
    x0, y0, x1, y1 = (int(round(v)) for v in box)
    for x in range(x0, x1, dash + gap):
        draw.line([(x, y0), (min(x + dash, x1), y0)], fill=colour, width=width)
        draw.line([(x, y1), (min(x + dash, x1), y1)], fill=colour, width=width)
    for y in range(y0, y1, dash + gap):
        draw.line([(x0, y), (x0, min(y + dash, y1))], fill=colour, width=width)
        draw.line([(x1, y), (x1, min(y + dash, y1))], fill=colour, width=width)


def draw_box(draw, box, state):
    """One of the ten, drawn the way the site draws it.

    The shapes carry the difference, not colour alone, exactly as on the page.
    """
    if state == "from_source":
        draw.rounded_rectangle(box, radius=6, fill=PUB)
    elif state == "not_collected":
        dashed_rect(draw, box, (90, 124, 110))
    elif state == "blank_in_source":
        draw.rounded_rectangle(box, radius=6, outline=PUB, width=3)
    elif state == "does_not_apply":
        draw.rounded_rectangle(box, radius=6, outline=PUB, width=3)
        draw.line([(box[0] + 4, box[3] - 4), (box[2] - 4, box[1] + 4)], fill=PUB, width=3)
    else:
        raise SystemExit(f"the panel holds a state the card cannot draw: {state}")


def build(f: dict) -> Image.Image:
    bold_path, regular_path = fonts()
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    kicker = ImageFont.truetype(bold_path, 19)
    head = ImageFont.truetype(bold_path, 54)
    sub = ImageFont.truetype(regular_path, 23)
    key = ImageFont.truetype(regular_path, 19)

    left, y = 56, 46
    draw.text((left, y), "A I   U S E   C A S E   R E G I S T E R   A U D I T",
              font=kicker, fill=INK_SOFT)
    y += 50

    # The headline, with the two figures in the accent the site uses for them.
    line_one = [("Of ", INK), (str(f["fields"]), ACCENT), (" boxes on the form,", INK)]
    line_two = [("the real entry answers ", INK), (str(f["answered"]), ACCENT), (".", INK)]
    for line in (line_one, line_two):
        x = left
        for text, colour in line:
            draw.text((x, y), text, font=head, fill=colour)
            x += draw.textlength(text, font=head)
        y += 66

    y += 14
    draw.text((left, y), "A published high-impact entry put through the field set this",
              font=sub, fill=INK_SOFT)
    draw.text((left, y + 32),
              f"audit proposes. It is one of {f['meeting_the_rule']} that meet the same rule.",
              font=sub, fill=INK_SOFT)
    y += 132

    # The ten boxes, in the panel's own order. Sized to sit between the text
    # above and the key below without a dead band under them.
    box_w, box_h, gap = 62, 104, 14
    for index, state in enumerate(f["states"]):
        x0 = left + index * (box_w + gap)
        draw_box(draw, (x0, y, x0 + box_w, y + box_h), state)

    # The key, drawn with the same shapes rather than with symbols, so a reader
    # matches it to the boxes above by looking rather than by guessing.
    foot = HEIGHT - 58
    draw.line([(left, foot - 26), (WIDTH - left, foot - 26)], fill=BORDER, width=1)
    x = left
    legend = [
        ("from_source", f"answered: {f['answered']}"),
        ("blank_in_source", f"asked, left empty: {f['asked_and_left_empty']}"),
        ("not_collected", f"never asked: {f['not_collected']}"),
    ]
    for state, label in legend:
        draw_box(draw, (x, foot, x + 18, foot + 22), state)
        draw.text((x + 28, foot + 1), label, font=key, fill=INK_SOFT)
        x += 28 + int(draw.textlength(label, font=key)) + 34

    tail = "saa2252.github.io"
    draw.text((WIDTH - left - draw.textlength(tail, font=key), foot + 1),
              tail, font=key, fill=INK)
    return image


def main() -> int:
    f = figures()
    ASSETS.mkdir(parents=True, exist_ok=True)
    build(f).save(ASSETS / "card.png", "PNG", optimize=True)
    bold_path, _ = fonts()
    stamp = dict(f, font=Path(bold_path).name, size=[WIDTH, HEIGHT])
    (ASSETS / "card.stamp").write_text(
        json.dumps(stamp, sort_keys=True) + "\n", encoding="utf-8")
    size = (ASSETS / "card.png").stat().st_size
    print(f"card.png written, {WIDTH}x{HEIGHT}, {size:,} bytes")
    print("figures: " + ", ".join(f"{k}={v}" for k, v in f.items() if k != "states"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
