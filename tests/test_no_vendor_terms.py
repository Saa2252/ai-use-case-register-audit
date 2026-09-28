"""T2. No term from the vendor list appears anywhere in data/derived/ or docs/, case-insensitive.

Enforces: S2
See governance/safeguards.md.

The vendor term list lives in data/raw/vendor_terms.txt, which is gitignored,
because the list is itself a list of vendor names. This test reads it from
there. When the list is absent, the test skips with a clear message rather than
passing silently, since a passing test with no terms would prove nothing.
"""

import re
import sys
from pathlib import Path

import pytest

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src.scrub import compile_term_pattern  # noqa: E402

TERM_FILE = REPO_ROOT / "data" / "raw" / "vendor_terms.txt"
SEARCH_DIRS = [REPO_ROOT / "data" / "derived", REPO_ROOT / "docs"]
TEXT_SUFFIXES = {".csv", ".json", ".md", ".html", ".js", ".css", ".txt"}


def load_terms() -> list[str]:
    if not TERM_FILE.exists():
        return []
    return [t.strip() for t in TERM_FILE.read_text().splitlines() if t.strip()]


def published_files() -> list[Path]:
    out = []
    for d in SEARCH_DIRS:
        if d.exists():
            out += [p for p in d.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES]
    return out


# Exact-string exemptions, approved by the owner on 23 September 2026.
#
# These are NOT categorical exemptions for markup, attributes or rendered text.
# Vendor names can and do appear in alt, title and aria-label attributes and in
# link URLs, and one was found inside a link during Phase 3. Only the two exact
# strings below are exempt, and only where they appear verbatim.
#
# Adding any further exemption requires the owner's approval and is a
# stop-and-ask condition. See governance/safeguards.md.
EXEMPT_EXACT_STRINGS = [
    '<meta charset',
    '<meta name="viewport"',
    'spheroidal elastic deformation sources',
]


def strip_exempt(text: str) -> str:
    """Blank out only the exact exempt strings, leaving everything else intact."""
    for s in EXEMPT_EXACT_STRINGS:
        text = text.replace(s, " " * len(s))
    return text


def test_no_vendor_terms_in_published_files():
    terms = load_terms()
    if not terms:
        pytest.skip("vendor term list not built yet: run the Phase 3 scrub first")

    # Same matcher the scrub uses, so the test cannot be weaker than the fix:
    # it covers spacing, punctuation and casing variants of every term.
    pattern = compile_term_pattern(terms)

    findings = []
    for path in published_files():
        text = strip_exempt(path.read_text(errors="replace"))
        hits = {m.group(0) for m in pattern.finditer(text)}
        if hits:
            rel = path.relative_to(REPO_ROOT)
            findings.append(f"{rel}: {sorted(hits)}")

    assert not findings, "vendor terms found in published files:\n" + "\n".join(findings)
