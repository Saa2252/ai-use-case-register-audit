"""The site works when served from a project subpath, not only from a root.

GitHub Pages serves a project site from a subpath such as /repository-name/.
A link or fetch beginning with a slash resolves to the domain root instead and
silently fetches nothing, which on this site would show the load-failure message
rather than an error anyone could diagnose.

These checks are cheap and they run before deployment rather than after it.
"""

import re

from conftest import REPO_ROOT

DOCS = REPO_ROOT / "docs"


def test_no_root_absolute_paths():
    problems = []
    for path in sorted(DOCS.rglob("*")):
        if not path.is_file() or path.suffix not in {".html", ".js", ".css"}:
            continue
        text = path.read_text()
        for match in re.finditer(r'(?:href|src)="(/[^/"][^"]*)"', text):
            problems.append(f"{path.name}: {match.group(1)}")
        for match in re.finditer(r'fetch\("(/[^"]*)"', text):
            problems.append(f"{path.name}: fetch {match.group(1)}")
    assert not problems, (
        "paths that assume the site is at a domain root:\n" + "\n".join(problems))


def test_jekyll_is_switched_off():
    """Without this file the host runs Jekyll, which skips some paths."""
    assert (DOCS / ".nojekyll").exists(), "docs/.nojekyll is missing"


def test_no_file_is_too_large_to_serve_comfortably():
    """Nothing here should be a slow download on a phone."""
    oversized = [
        f"{p.relative_to(DOCS)}: {p.stat().st_size / 1024 / 1024:.1f} MB"
        for p in sorted(DOCS.rglob("*"))
        if p.is_file() and p.stat().st_size > 5 * 1024 * 1024
    ]
    assert not oversized, "files larger than 5 MB:\n" + "\n".join(oversized)
