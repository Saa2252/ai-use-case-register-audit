"""T9. Exactly three HTML pages in docs/. No database files. No login code.

Enforces: S12
See governance/safeguards.md.
"""

import re

from conftest import REPO_ROOT

DB_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".mdb", ".accdb"}
LOGIN_PATTERNS = [r"\blogin\b", r"\bsign[\s-]?in\b", r"\bpassword\b", r"\bauthenticat", r"\bsession\b"]


def test_exactly_three_pages():
    pages = sorted(p.name for p in (REPO_ROOT / "docs").glob("*.html"))
    assert len(pages) == 3, f"expected three pages, found {pages}"


def test_no_database_files():
    found = [str(p.relative_to(REPO_ROOT)) for p in REPO_ROOT.rglob("*")
             if p.is_file() and p.suffix in DB_SUFFIXES and ".venv" not in p.parts]
    assert not found, f"database files present: {found}"


def test_no_login_code():
    found = []
    for p in sorted((REPO_ROOT / "docs").rglob("*")):
        if p.is_file() and p.suffix in {".html", ".js"}:
            text = p.read_text()
            for pat in LOGIN_PATTERNS:
                if re.search(pat, text, re.I):
                    found.append(f"{p.name}: {pat}")
    assert not found, f"login-like code on the site: {found}"
