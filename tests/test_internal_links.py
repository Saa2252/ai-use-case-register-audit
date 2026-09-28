"""Every internal link resolves, and a query string reaches a page that reads it.

A broken link to a missing page is loud: the browser shows an error. The failure
this test exists for is the quiet one. A link carrying a filter, such as a band
selection, can point at a page that exists and simply ignores the query. Nothing
errors. The reader sees the wrong view with the filter apparently not working,
and no test notices.

That becomes possible the moment a page is renamed, which is why this test is
written before the rename rather than after it.
"""

import re

from conftest import REPO_ROOT

DOCS = REPO_ROOT / "docs"
EXTERNAL = re.compile(r"^(?:https?:|mailto:|#|tel:)", re.I)


def pages():
    return sorted(DOCS.glob("*.html"))


def scripts():
    return sorted((DOCS / "assets").glob("*.js"))


# Links the scripts build at run time. These never appear in the HTML, so a scan
# of the pages alone does not see them. They are the links most likely to break
# on a rename, because they are the ones a search of the markup will not find.
LINK_IN_SCRIPT = re.compile(r'["\']([A-Za-z0-9_./-]+\.html)(\?[A-Za-z0-9_=&%.+-]*)?["\']')


def runtime_links():
    found = []
    for script in scripts():
        text = script.read_text()
        for match in LINK_IN_SCRIPT.finditer(text):
            found.append((script.name, match.group(1), (match.group(2) or "").lstrip("?")))
    return found


def script_sources(page_text: str) -> list[str]:
    """The scripts a page loads, with any cache stamp taken off."""
    return [src.split("?")[0] for src in re.findall(r'<script src="([^"]+)"', page_text)]


def test_links_built_by_scripts_resolve_and_are_read():
    """The links the pages build at run time, which a scan of the markup misses."""
    problems = []
    for origin, target, query in runtime_links():
        destination = DOCS / target
        if not destination.exists():
            problems.append(f"{origin} builds a link to {target}: no such file")
            continue
        if not query:
            continue
        loaded = "\n".join(
            (DOCS / src).read_text()
            for src in script_sources(destination.read_text())
            if (DOCS / src).exists()
        )
        for name in {pair.split("=")[0] for pair in query.split("&") if pair}:
            if not re.search(r'get\(\s*["\']' + re.escape(name) + r'["\']', loaded):
                problems.append(
                    f"{origin} builds {target}?{name}=, but {target} does not read '{name}'")
    assert not problems, (
        "links built by scripts that do not resolve or are ignored:\n" + "\n".join(problems))


def test_scripts_do_build_some_links():
    """Guard against the check above passing because it found nothing to check."""
    assert runtime_links(), (
        "no run-time links found: the pattern no longer matches how links are built, "
        "so the check above proves nothing"
    )


def test_every_internal_link_resolves():
    problems = []
    for page in pages():
        text = page.read_text()
        for href in re.findall(r'href="([^"]+)"', text):
            if EXTERNAL.match(href):
                continue
            target = href.split("?")[0].split("#")[0]
            if not target:
                continue
            if not (DOCS / target).exists():
                problems.append(f"{page.name} -> {href}: no such file")
    assert not problems, "internal links that do not resolve:\n" + "\n".join(problems)


def test_every_query_string_reaches_a_page_that_reads_it():
    """A filter link must land on a page whose scripts read that parameter.

    Only links between pages are checked. A stylesheet or script carrying a
    cache stamp is not a filter, and the file it points at is not expected to
    read anything.
    """
    problems = []
    for page in pages():
        text = page.read_text()
        for href in re.findall(r'href="([^"]+)"', text):
            if EXTERNAL.match(href) or "?" not in href:
                continue
            target, query = href.split("?", 1)
            target = target.split("#")[0]
            if not target.endswith(".html"):
                continue
            destination = DOCS / target
            if not destination.exists():
                problems.append(f"{page.name} -> {href}: no such file")
                continue
            names = {pair.split("=")[0] for pair in query.split("&") if pair}
            loaded = "\n".join((DOCS / src).read_text() for src in script_sources(destination.read_text())
                               if (DOCS / src).exists())
            for name in names:
                if not re.search(r'get\(\s*["\']' + re.escape(name) + r'["\']', loaded):
                    problems.append(
                        f"{page.name} -> {href}: {target} does not read the '{name}' parameter")
    assert not problems, (
        "links carrying a filter that the destination ignores:\n" + "\n".join(problems))


def test_scripts_a_page_loads_all_exist():
    problems = []
    for page in pages():
        for src in script_sources(page.read_text()):
            if not (DOCS / src).exists():
                problems.append(f"{page.name}: {src}")
    assert not problems, "pages loading scripts that are not published:\n" + "\n".join(problems)
