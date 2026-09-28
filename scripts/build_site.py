"""Build the three site pages from one template.

Header, navigation and footer are written once here, so they cannot drift
between pages. Every figure in the body is a data-figure placeholder filled at
load time from docs/data (S5). No number is typed into the HTML.
"""

import hashlib
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.disclaimer import (AUTHORSHIP, DISCLAIMER, ONTARIO_ATTRIBUTION,
                            ONTARIO_LICENCE_URL)

DOCS = REPO_ROOT / "docs"
NAV = [("index.html", "Register"), ("gaps.html", "Gaps"), ("obligations.html", "Oversight pack")]


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


def data_stamp() -> str:
    """One stamp covering every published data file.

    The scripts fetch these at runtime, so a page can be perfectly up to date
    while the browser serves yesterday's figures from its cache. Stamping the
    assets alone was not enough: the data changes more often than the code.
    """
    digest = hashlib.sha256()
    for path in sorted((DOCS / "data").glob("*.json")):
        digest.update(path.read_bytes())
    return "".join(chr(ord("a") + int(ch, 16)) for ch in digest.hexdigest()[:8])


def page(file, title, heading, lede, body, scripts="", ontario=False):
    links = []
    for href, label in NAV:
        current = ' aria-current="page"' if href == file else ""
        links.append('    <a href="' + href + '"' + current + ">" + label + "</a>")
    ontario_line = ""
    if ontario:
        ontario_line = ('\n  <p id="ontario-attribution">' + ONTARIO_ATTRIBUTION +
                        ' <a href="' + ONTARIO_LICENCE_URL + '">Licence</a></p>')
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>" + title + "</title>\n"
        '<link rel="stylesheet" href="' + stamp("assets/style.css") + '">\n</head>\n<body>\n'
        '<div class="wrap" data-dv="' + data_stamp() + '">\n\n'
        "<header>\n  <h1>AI Use Case Register Audit</h1>\n"
        '  <p class="lede">An independent read of publicly published AI use case inventories.</p>\n'
        "  <nav>\n" + "\n".join(links) + "\n  </nav>\n</header>\n\n"
        "<main>\n  <h2>" + heading + "</h2>\n"
        '  <p class="lede">' + lede + "</p>\n" + body + "\n</main>\n\n"
        '<footer>\n  <p id="disclaimer">' + DISCLAIMER + "</p>" + ontario_line +
        "\n  <p>" + AUTHORSHIP + "</p>\n</footer>\n\n</div>\n"
        '<script src="' + stamp("assets/figures.js") + '"></script>' + scripts + "\n</body>\n</html>\n"
    )


def main() -> None:
    bodies = (REPO_ROOT / "scripts" / "bodies")
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(page(
        "index.html", "Register | AI Use Case Register Audit", "The register",
        "The list the United States federal government publishes of the AI systems it uses.",
        (bodies / "view1.html").read_text(),
        scripts='\n<script src="' + stamp("assets/register.js") + '"></script>'))
    (DOCS / "gaps.html").write_text(page(
        "gaps.html", "Gaps | AI Use Case Register Audit", "What the register does not tell you",
"Where this register is incomplete, and where it is easy to read wrongly.",
        (bodies / "view2.html").read_text(),
        scripts='\n<script src="' + stamp("assets/views.js") + '"></script>'
                '\n<script src="' + stamp("assets/tabs.js") + '"></script>', ontario=True))
    (DOCS / "obligations.html").write_text(page(
        "obligations.html", "Oversight pack | AI Use Case Register Audit",
        "If someone asked about the riskiest systems",
        "What this register could hand over about the systems it flags high-impact, if someone asked.",
        (bodies / "view3.html").read_text(),
        scripts='\n<script src="' + stamp("assets/views.js") + '"></script>'))
    print("three pages written to docs/")


if __name__ == "__main__":
    main()
