"""T9. Exactly three HTML pages in docs/. No database files. No login code.

Enforces: S12
See governance/safeguards.md.
"""

import re

from conftest import REPO_ROOT

DB_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".mdb", ".accdb"}
LOGIN_PATTERNS = [r"\blogin\b", r"\bsign[\s-]?in\b", r"\bpassword\b", r"\bauthenticat", r"\bsession\b"]


# The brief set three views. Two additions were approved and recorded in the
# scope-change table in governance/safeguards.md: a design view, and then the
# decision to merge the planned dashboard into that page rather than add a
# fifth. Four is the approved number.
APPROVED_PAGES = {"index.html", "register.html", "gaps.html", "obligations.html"}


def test_exactly_the_approved_pages():
    pages = {p.name for p in (REPO_ROOT / "docs").glob("*.html")}
    assert pages == APPROVED_PAGES, (
        f"pages present: {sorted(pages)}, approved: {sorted(APPROVED_PAGES)}")


def test_no_database_files():
    found = [str(p.relative_to(REPO_ROOT)) for p in REPO_ROOT.rglob("*")
             if p.is_file() and p.suffix in DB_SUFFIXES and ".venv" not in p.parts]
    assert not found, f"database files present: {found}"


def test_no_login_code():
    """The site and the application both. S12 bans a login on either."""
    found = []
    sources = sorted((REPO_ROOT / "docs").rglob("*")) + sorted((REPO_ROOT / "app").rglob("*"))
    for p in sources:
        if p.is_file() and p.suffix in {".html", ".js", ".py"}:
            text = p.read_text()
            for pat in LOGIN_PATTERNS:
                if re.search(pat, text, re.I):
                    found.append(f"{p.name}: {pat}")
    assert not found, f"login-like code on the site: {found}"
