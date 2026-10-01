"""Build the three site pages from one template.

Header, navigation and footer are written once here, so they cannot drift
between pages. Every figure in the body is a data-figure placeholder filled at
load time from docs/data (S5). No number is typed into the HTML.
"""

import hashlib
import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.statements import apply as apply_statements  # noqa: E402
from src.disclaimer import (AUTHORSHIP, DISCLAIMER, ONTARIO_ATTRIBUTION,
                            ONTARIO_LICENCE_URL, SITE_URL, UK_ATTRIBUTION,
                            UK_LICENCE_URL)

# Each licence that asks for an attribution statement, and the pages it goes
# on. A page carries the statement for every source whose material it shows.
# Both statements are copied verbatim from their licence pages and neither is
# paraphrased (S1).
ATTRIBUTIONS = {
    "ontario": (ONTARIO_ATTRIBUTION, ONTARIO_LICENCE_URL),
    "uk": (UK_ATTRIBUTION, UK_LICENCE_URL),
}

DOCS = REPO_ROOT / "docs"
# The site has two halves, and the navigation says so. Three pages read the
# register as published. One says what the author would build from what they
# found. Presented as four equal tabs, the fourth reads as an afterthought at
# the end of a long audit rather than the other half of the work.
NAV_GROUPS = [
    ("What I would build", [
        ("index.html", "The field set"),
        ("keeping.html", "Keeping it current"),
    ]),
    ("What the register says", [
        ("register.html", "The register"),
        ("gaps.html", "What it does not tell you"),
        ("obligations.html", "The oversight pack"),
    ]),
]

NAV = [entry for _, entries in NAV_GROUPS for entry in entries]


def stamp(relative: str) -> str:
    """A short content hash appended to an asset URL.

    Without it a browser keeps serving the copy it already has, and an edit to
    the stylesheet or a script is invisible until someone clears their cache.
    That has now caused three separate rounds of confusion, each one looking
    like a broken feature rather than a stale file.
    """
    path = DOCS / relative
    if not path.exists():
        return relative
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:8]
    # Rendered with letters only. A hexadecimal stamp contains digit runs, and
    # the safeguard forbidding numbers in the markup would flag them, correctly
    # by its own rule and pointlessly in substance. Removing the digits removes
    # the collision rather than carving an exception into the check.
    letters = "".join(chr(ord("a") + int(ch, 16)) for ch in digest)
    return relative + "?v=" + letters


# The stamp is written here as well as into every page, and this file is left
# out of the hash so that writing it does not change it.
STAMP_FILE = "build_stamp.json"


def data_stamp() -> str:
    """One stamp covering every published data file.

    The scripts fetch these at runtime, so a page can be perfectly up to date
    while the browser serves yesterday's figures from its cache. Stamping the
    assets alone was not enough: the data changes more often than the code.
    """
    digest = hashlib.sha256()
    for path in sorted((DOCS / "data").glob("*.json")):
        if path.name == STAMP_FILE:
            continue
        digest.update(path.read_bytes())
    return "".join(chr(ord("a") + int(ch, 16)) for ch in digest.hexdigest()[:8])


def write_stamp(stamp: str) -> None:
    """Publish the stamp beside the data, so a page can check it belongs.

    The query stamp on each data file stops a browser serving yesterday's
    figures to today's page. It does nothing about the other direction, which
    is the one that actually happened: the host caches HTML for ten minutes, so
    for ten minutes after a deployment a returning visitor can hold yesterday's
    markup while the data files it asks for come back current. A query string
    is a cache key, not a version, so the server answers with the new file.

    The result is a page whose markup and data are from different builds. It
    does not look broken. It looks like a register with values missing, which
    is the one thing this site must never look like by accident.

    Writing the stamp here lets a page compare what it was built against with
    what it just received, and say so when they differ.
    """
    (DOCS / "data" / STAMP_FILE).write_text(
        json.dumps({"stamp": stamp}) + "\n", encoding="utf-8")


# What a link to this site looks like when it is pasted somewhere else.
#
# A preview card travels with none of the page around it: no selection rule
# beside it, no caveat under it. So the description is the page's own lede,
# which is copy already approved and already published above the fold, rather
# than a second description written for the card and approved nowhere.
#
# The picture is drawn by scripts/build_card.py from the published findings and
# names no organisation, for the same reason.
#
# The addresses here are absolute because a scraper reads this page from
# another host, where a relative address resolves against that host. That is
# what made these tags need the exact-string exemption the owner approved on
# 2 October 2026, recorded in governance/safeguards.md.
#
# The image's dimensions are deliberately not declared. They would be two
# numbers typed into every page, which is the thing S5 exists to stop, and the
# host fetches the picture and measures it anyway.
CARD = "assets/card.png"
TAGLINE = "An independent read of publicly published AI use case inventories."


def preview(file, title, heading, lede) -> str:
    description = (lede or TAGLINE).strip()
    address = SITE_URL + ("" if file == "index.html" else file)
    tags = [
        ("og:type", "website"),
        ("og:site_name", "AI Use Case Register Audit"),
        ("og:title", heading or title),
        ("og:description", description),
        ("og:url", address),
        ("og:image", SITE_URL + CARD),
        ("og:image:alt", "Two forms side by side. The left is a published entry with "
                         "most of its ten boxes empty. The right is a made-up entry with "
                         "every box resolved."),
        ("twitter:card", "summary_large_image"),
        ("twitter:title", heading or title),
        ("twitter:description", description),
        ("twitter:image", SITE_URL + CARD),
    ]
    return "".join(
        '<meta property="' + name + '" content="' + value.replace('"', "&quot;") + '">\n'
        for name, value in tags)


def page(file, title, heading, lede, body, scripts="", licences=(), figures=True,
         page_class=""):
    links = []
    for index, (group_label, entries) in enumerate(NAV_GROUPS):
        kind = "audit" if index == 0 else "design"
        links.append('    <div class="navgroup ' + kind + '">')
        links.append('      <span class="navlabel">' + group_label + "</span>")
        links.append('      <span class="navlinks">')
        for href, label in entries:
            current = ' aria-current="page"' if href == file else ""
            links.append('        <a href="' + href + '"' + current + ">" + label + "</a>")
        links.append("      </span>")
        links.append("    </div>")
    attribution_lines = ""
    for name in licences:
        statement, url = ATTRIBUTIONS[name]
        attribution_lines += ('\n  <p id="' + name + '-attribution">' + statement +
                              ' <a href="' + url + '">Licence</a></p>')
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>" + title + "</title>\n"
        + preview(file, title, heading, lede) +
        '<link rel="stylesheet" href="' + stamp("assets/style.css") + '">\n</head>\n<body>\n'
        '<div class="wrap" data-dv="' + data_stamp() + '">\n\n'
        "<header>\n  <h1>AI Use Case Register Audit</h1>\n"
        '  <p class="lede">An independent read of publicly published AI use case inventories.</p>\n'
        "  <nav>\n" + "\n".join(links) + "\n  </nav>\n</header>\n\n"
        "<main" + (' class="' + page_class + '"' if page_class else "") + ">\n  <h2>" + heading + "</h2>\n"
        + ('  <p class="lede">' + lede + "</p>\n" if lede else "") + apply_statements(body) + "\n</main>\n\n"
        '<footer>\n  <p id="disclaimer">' + DISCLAIMER + "</p>" + attribution_lines +
        "\n  <p>" + AUTHORSHIP + "</p>\n</footer>\n\n</div>\n"
        + (('<script src="' + stamp("assets/figures.js") + '"></script>') if figures else "")
        + scripts + "\n</body>\n</html>\n"
    )


def main() -> None:
    bodies = (REPO_ROOT / "scripts" / "bodies")
    DOCS.mkdir(exist_ok=True)
    write_stamp(data_stamp())
    # The fifth page. Its own data file, its own script, and no findings loaded,
    # because nothing on it was counted from a published file and it must never
    # be filled with a figure from the audit.
    (DOCS / "keeping.html").write_text(page(
        "keeping.html", "Keeping it current | AI Use Case Register Audit",
        "Keeping a register current",
        "A proposal for how a register would be kept up, written against the five "
        "things the field set does not do. Not tested against any real register.",
        (bodies / "view5.html").read_text(),
        figures=False,
        page_class="design-page",
        scripts='\n<script src="' + stamp("assets/keeping.js") + '"></script>'))
    (DOCS / "register.html").write_text(page(
        "register.html", "The register | AI Use Case Register Audit", "The register",
        "The list the United States federal government publishes of the AI systems it uses.",
        (bodies / "view1.html").read_text(),
        scripts='\n<script src="' + stamp("assets/register.js") + '"></script>'))
    (DOCS / "gaps.html").write_text(page(
        "gaps.html", "Gaps | AI Use Case Register Audit", "What the register does not tell you",
"What this register does not record, and where it is easy to read wrongly.",
        (bodies / "view2.html").read_text(),
        scripts='\n<script src="' + stamp("assets/views.js") + '"></script>'
                '\n<script src="' + stamp("assets/summary.js") + '"></script>', licences=("ontario", "uk")))
    (DOCS / "obligations.html").write_text(page(
        "obligations.html", "Oversight pack | AI Use Case Register Audit",
        "If someone asked about the riskiest systems",
        "What this register could hand over about the systems it flags high-impact, if someone asked.",
        (bodies / "view3.html").read_text(),
        scripts='\n<script src="' + stamp("assets/views.js") + '"></script>'))
    (DOCS / "index.html").write_text(page(
        "index.html", "AI Use Case Register Audit",
        # The page heading is the first sentence of the opening, not a label for
        # the page. A stranger meets the fact before anything about this project.
        "The US government publishes a list of the AI systems its agencies use",
        "",
        (bodies / "view4.html").read_text(),
        # This page fills its own figures from the field set, so it does not load
        # the findings filler as well. Two scripts writing the same elements race,
        # and the loser leaves "unavailable" on screen.
        figures=False,
        # Colour on this page means one of two things and nothing else, so the
        # rules that carry that meaning are scoped to the page rather than let
        # loose on the three audit pages.
        page_class="design-page",
        # Every field card on this page states what the UK standard asks, read
        # from its published template, so the page carries that licence's
        # attribution statement.
        licences=("uk",),
        scripts='\n<script src="' + stamp("assets/proposal.js") + '"></script>'))
    # Counted, not written out, so the message cannot drift from the fact when
    # a page is added or removed.
    print(str(len(list(DOCS.glob("*.html")))) + " pages written to docs/")


if __name__ == "__main__":
    main()
