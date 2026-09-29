"""Build the social preview card at docs/assets/preview.png.

A crawler reading a link does not run JavaScript, so a preview card cannot
fetch its figure the way the pages do. The figure is therefore drawn into the
image here, at build time, read from data/derived like every other number this
project publishes. It is generated, never typed.

The owner was shown the alternative on 30 September 2026, which was to put the
figure in the card's description text instead. That would have meant a literal
number in the page head, and widening T5 from "no digits in published HTML" to
"no digits except the ones the build put there". The owner expressed no
preference, so the developer took the narrower option: the description carries
no numerals and T5 is untouched. Recorded as a delegated call in
governance/safeguards.md, not as an owner ruling.

Run:  python scripts/build_preview.py
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

DERIVED = REPO_ROOT / "data" / "derived"
OUT = REPO_ROOT / "docs" / "assets" / "preview.png"

# What the card measures. The size every social platform expects.
WIDTH, HEIGHT = 1200, 630
MARGIN = 80

# The site's own light palette, from docs/assets/style.css. The card cannot
# follow a reader's dark mode, so it commits to the light one.
PAPER = (251, 251, 249)
INK = (28, 27, 24)
INK_SOFT = (87, 84, 76)
PUB = (23, 80, 108)
HAIR = (217, 215, 208)


def font(size: int, bold: bool = False):
    """A face that exists on this machine, falling back rather than failing."""
    candidates = [
        "/System/Library/Fonts/Supplemental/" + ("Georgia Bold.ttf" if bold else "Georgia.ttf"),
        "/System/Library/Fonts/Supplemental/" + ("Arial Bold.ttf" if bold else "Arial.ttf"),
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans" + ("-Bold" if bold else "") + ".ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default(size)


def wrap(draw, text: str, face, width: int) -> list:
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=face) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def main() -> int:
    fieldset = json.loads((DERIVED / "fieldset.json").read_text(encoding="utf-8"))
    lead = fieldset["lead"]

    card = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(card)

    y = MARGIN

    draw.text((MARGIN, y), "AI USE CASE REGISTER AUDIT", font=font(22, True), fill=PUB)
    y += 60

    # The figure, read from the data. Nothing on this card is typed.
    figure = f"{lead['no_oversight']:,} of {lead['high_impact']:,}"
    draw.text((MARGIN, y), figure, font=font(104, True), fill=INK)
    y += 140

    for line in wrap(
        draw,
        "entries marked high-impact in the 2025 US federal AI register leave all "
        "nine oversight questions blank.",
        font(38),
        WIDTH - 2 * MARGIN,
    ):
        draw.text((MARGIN, y), line, font=font(38), fill=INK)
        y += 52

    y += 26
    draw.line([(MARGIN, y), (WIDTH - MARGIN, y)], fill=HAIR, width=2)
    y += 28

    draw.text(
        (MARGIN, y),
        "A filled field shows information was provided, not that the practice "
        "is adequate.",
        font=font(23),
        fill=INK_SOFT,
    )

    draw.text(
        (MARGIN, HEIGHT - MARGIN + 6),
        "An independent portfolio project. Not affiliated with any government body.",
        font=font(21),
        fill=INK_SOFT,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    card.save(OUT, "PNG", optimize=True)
    print(f"{OUT.relative_to(REPO_ROOT)}  {WIDTH}x{HEIGHT}  {OUT.stat().st_size:,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
