"""Build the vendor term list, remove vendor and product mentions, drop contact fields.

Phase 3. Enforces S2 (no vendor or product names) and S8 (no personal data).

Nothing in this module writes a vendor term to a committed file. The term list
lives in data/raw/, which is gitignored, because the list is itself a list of
vendor names. Only counts of what was removed are published.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW = REPO_ROOT / "data" / "raw"
DERIVED = REPO_ROOT / "data" / "derived"

# A value that means "nothing selected" rather than "not answered".
# Two 2025 fields store an empty multi-select as the literal text "[]".
EMPTY_VALUES = {"", "[]", "['']", '[""]', "nan", "none", "n/a", "na"}

PLACEHOLDER_PATTERNS = [
    r"^n\s*/?\s*a$", r"^none$", r"^not applicable$", r"^tbd$", r"^to be determined$",
    r"^unknown$", r"^pending$", r"^\.+$", r"^-+$", r"^x+$", r"^test$", r"^n\.a\.$",
]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[-. ]?)?\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}(?!\d)")

# Terms too short or too ordinary to match safely on their own. A vendor term
# that is also an ordinary English word would scrub legitimate prose.
STOPWORDS = {
    "ai", "the", "and", "for", "inc", "llc", "corp", "co", "ltd", "group", "systems",
    "system", "software", "services", "service", "solutions", "technologies",
    "technology", "data", "cloud", "platform", "suite", "tools", "tool", "team",
    "office", "center", "centre", "agency", "federal", "national", "us", "usa",
    "gov", "government", "department", "enterprise", "analytics", "digital",
    "information", "management", "research", "development", "security", "network",
    "application", "applications", "program", "project", "model", "models", "api",
    "open", "source", "web", "online", "mobile", "desktop", "server", "database",
    "new", "other", "none", "various", "internal", "custom", "general", "commercial",
}

MIN_TERM_LENGTH = 4


def is_empty(value) -> bool:
    """True when a cell carries no answer, including the literal empty list."""
    return str(value).strip().lower() in EMPTY_VALUES or str(value).strip() == ""


def split_terms(value: str) -> list[str]:
    """Split one vendor or product cell into candidate terms."""
    if is_empty(value):
        return []
    parts = re.split(r"[;,/|]|\band\b|\n|\[|\]|'|\"", str(value))
    out = []
    for p in parts:
        p = re.sub(r"[^\w\s.&-]", " ", p).strip(" .-")
        p = re.sub(r"\s+", " ", p)
        if len(p) >= MIN_TERM_LENGTH and p.lower() not in STOPWORDS:
            out.append(p)
    return out


def build_term_list(series_list) -> list[str]:
    """Collect distinct vendor and product terms from the given columns.

    Terms shorter than MIN_TERM_LENGTH, and terms that are ordinary words, are
    dropped, because scrubbing on them would damage legitimate prose.
    """
    terms = set()
    for s in series_list:
        for v in s.dropna():
            terms.update(split_terms(v))
    cleaned = {t for t in terms if len(t) >= MIN_TERM_LENGTH and t.lower() not in STOPWORDS}
    return sorted(cleaned, key=lambda t: (-len(t), t.lower()))


# Separators tolerated between the parts of a term. A product written
# "OpenAI" in one field appears as "Open AI" in another, and a product named
# in a use case title can be broken by punctuation, as in "(VAO) Ally".
_SEP = r"[\s\-_./()]{0,3}"


def _split_parts(term: str) -> list[str]:
    """Split a term into the chunks that must appear in order.

    Splits only on separators already present in the term. Camel-case splitting
    was removed by the owner on 23 September 2026: it made any product whose
    name is two ordinary words joined together match those two ordinary words in
    running prose, which produced about 55 false positives on its own.
    """
    parts = [c for c in re.split(r"[\s\-_./()]+", term) if c]
    return parts or [term]


def term_regex(term: str) -> str:
    """Regex for one term, tolerant of spacing, punctuation and casing."""
    parts = _split_parts(term)
    return _SEP.join(re.escape(p) for p in parts)


def compile_term_pattern(terms: list[str]) -> re.Pattern | None:
    """One case-insensitive pattern covering spacing and casing variants.

    Longest terms first, so the most specific match wins.
    """
    if not terms:
        return None
    ordered = sorted(terms, key=lambda t: (-len(t), t.lower()))
    return re.compile(r"\b(" + "|".join(term_regex(t) for t in ordered) + r")\b", re.I)


def scrub_text(value, pattern: re.Pattern | None) -> tuple[str, int]:
    """Replace vendor mentions with [product]. Returns the text and a count."""
    if value is None or is_empty(value) or pattern is None:
        return ("" if value is None else str(value)), 0
    text = str(value)
    new, n = pattern.subn("[product]", text)
    return new, n


def scrub_personal(value) -> tuple[str, int, int]:
    """Remove email addresses and phone numbers from free text."""
    if value is None:
        return "", 0, 0
    text = str(text_or_empty(value))
    text, e = EMAIL_RE.subn("[contact removed]", text)
    text, p = PHONE_RE.subn("[contact removed]", text)
    return text, e, p


def text_or_empty(value) -> str:
    return "" if value is None else str(value)


def is_placeholder(value) -> bool:
    """True when a cell holds a filler value rather than a real answer."""
    v = str(value).strip().lower()
    if not v:
        return False
    return any(re.match(p, v) for p in PLACEHOLDER_PATTERNS)


# --- URL handling (owner decision, 23 September 2026: option 2) -------------
#
# A URL containing a vendor term is replaced whole, and what it was is kept.
# Scrubbing only the host leaves something shaped like a working link, which a
# reader may try, cite, or take as evidence the link was checked. Replacing the
# whole URL removes that, and naming the kind of link preserves the fact that
# the entry supplied one, which the completeness figures depend on.

URL_RE = re.compile(r"https?://[^\s,;\"'<>()\]]+", re.I)

URL_KIND = {
    "code_url": "code repository",
    "link_to_data": "data source",
    "pia_url": "privacy impact assessment",
}


def scrub_urls(value, column: str, pattern: "re.Pattern | None") -> tuple[str, int]:
    """Replace any URL containing a blocklist term, keeping what it was.

    Returns the text and the number of URLs replaced.
    """
    if value is None or pattern is None:
        return ("" if value is None else str(value)), 0
    text = str(value)
    kind = URL_KIND.get(column)
    label = f"[link removed: {kind}]" if kind else "[link removed]"

    count = 0

    def repl(match: re.Match) -> str:
        nonlocal count
        url = match.group(0)
        if pattern.search(url):
            count += 1
            return label
        return url

    return URL_RE.sub(repl, text), count
