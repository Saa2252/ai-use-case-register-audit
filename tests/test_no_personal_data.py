"""T8. No email addresses or phone numbers appear in derived data or on the site.

Enforces: S8
See governance/safeguards.md.
"""

import re
from pathlib import Path

from conftest import REPO_ROOT

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}(?!\d)")

SEARCH_DIRS = [REPO_ROOT / "data" / "derived", REPO_ROOT / "docs"]
TEXT_SUFFIXES = {".csv", ".json", ".md", ".html", ".js", ".css", ".txt"}

# The disclaimer and licence text carry no contact details, but the site may
# legitimately reference an organisation. Nothing is exempt from this test today.
EXEMPT: set[str] = set()


def published_files() -> list[Path]:
    out = []
    for d in SEARCH_DIRS:
        if d.exists():
            out += [p for p in d.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES]
    return [p for p in out if str(p.relative_to(REPO_ROOT)) not in EXEMPT]


def test_no_personal_data():
    findings = []
    for path in published_files():
        text = path.read_text(errors="replace")
        rel = path.relative_to(REPO_ROOT)
        e = len(EMAIL_RE.findall(text))
        p = len(PHONE_RE.findall(text))
        if e:
            findings.append(f"{rel}: {e} email address(es)")
        if p:
            findings.append(f"{rel}: {p} phone-number pattern(s)")
    assert not findings, "personal data found in published files:\n" + "\n".join(findings)
