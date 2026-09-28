"""T4. No banned word from CLAUDE.md Section 8 appears in docs/, derived findings, the README or exports.

Also checks the banned trend framing added by the owner's addendum of
22 September 2026, which applies to the serious category only. See
governance/decision-rules.md section 4.

Enforces: S4, S10
See governance/safeguards.md.
"""

import pytest

from conftest import NOT_IMPLEMENTED

# CLAUDE.md Section 8. "withheld" is permitted only when quoting the source's
# own exclusion rules, which the implementation must allow for.
BANNED_WORDS = [
    "failed",
    "failure to",
    "hid",
    "hidden",
    "concealed",
    "withheld",
    "negligent",
    "violated",
    "violation",
    "non-compliant",
    "compliant",
    "illegal",
    "unlawful",
    "breach",
    "misconduct",
    "worst",
    "best-performing",
    "ranked",
]

# Owner addendum, 22 September 2026. Global ban, not scoped to one category.
# No count in this project is a safe trend: inclusion criteria changed between
# years, consolidated off-the-shelf reporting is new in 2025, and the serious
# category was defined under a different OMB memorandum in each year.
#
# Matched as WHOLE WORDS, case-insensitively. Substring matching would wrongly
# catch ordinary words such as "prose", "fellow" and "jumper".
BANNED_TREND_WORDS = [
    # The eight the owner set on 22 September 2026.
    "increased",
    "decreased",
    "rose",
    "fell",
    "doubled",
    "grew",
    "growth",
    "jump",
    # Base forms, added on the owner's standing offer to extend the list.
    # A word test catches these cheaply. A human reading at Phase 7 would not.
    "increase",
    "decrease",
    "rise",
    "fall",
    "grow",
]

# Deliberately NOT banned: "double". "Double counting" is the natural term for
# the M1 question of whether one capability is registered more than once, and
# the project needs it. "doubled" stays banned and whole-word matching keeps
# the two apart.

# Files exempt from BANNED_TREND_WORDS, set by the owner. These exist to state
# the rule. governance/safeguards.md is deliberately NOT exempt: it documents
# the ban by reference so it stays subject to it.
TREND_BAN_EXEMPT_PATHS = [
    "tests/test_banned_words.py",
    "CLAUDE.md",
    "governance/decision-rules.md",
]

# The crosswalk caveat, required verbatim wherever the entry-level year
# comparison appears.
REQUIRED_CROSSWALK_CAVEAT = (
    "A change in classification may reflect the new definition or an agency "
    "reassessment. The data cannot separate the two."
)


SCOPE_GLOBS = ["docs/*.html", "docs/assets/*.js", "README.md",
               "data/derived/findings.json", "data/derived/reusability_findings.json",
               "data/derived/oversight_information_pack.md"]

# "withheld" is permitted where it names the source's own exclusion mechanism,
# which is a published field of the register rather than a description of conduct.
WORD_EXEMPTIONS = {"withheld"}


def _scoped_files():
    from conftest import REPO_ROOT
    out = []
    for pattern in SCOPE_GLOBS:
        out += sorted(REPO_ROOT.glob(pattern))
    return [p for p in out if p.is_file()]


def test_no_banned_words():
    import re
    words = [w for w in BANNED_WORDS if w not in WORD_EXEMPTIONS]
    pattern = re.compile(r"\b(" + "|".join(re.escape(w) for w in words) + r")\b", re.I)
    findings = []
    for path in _scoped_files():
        for m in pattern.finditer(path.read_text()):
            findings.append(f"{path.name}: '{m.group(0)}'")
    assert not findings, "banned words in published copy:\n" + "\n".join(findings)


# --- Scope of the trend-word ban (owner ruling, 24 September 2026) ----------
#
# The ban exists to stop THIS PROJECT framing counts as a trend. Text written by
# the agencies and published in the register is data, not framing: a use case
# named "Fall Prediction Tool" frames nothing.
#
# The boundary is drawn by KEY, never by file path, because this project's own
# prose sits inside the same JSON files as the source values. A trend sentence
# written into a caveat is exactly what this test exists to catch, and excluding
# a whole file would let it through.
#
# Any key not listed here is treated as project prose and IS checked. A new field
# therefore lands on the checked side by default.
SOURCE_DATA_KEYS = {
    # docs/data/register_table.json: one entry per row, copied from the register
    "rows",
    # field names as the two registers publish them
    "field", "oversight_field_coverage",
    "field_completeness_all_rows", "field_completeness_high_impact",
    # the classification labels are the data's own wording
    "bands",
    # row positions, not text
    "entries_flagged_at_highest_threshold",
}

TREND_SUFFIXES = {".md", ".html", ".py", ".js", ".json", ".txt", ".ipynb"}
TREND_SKIP_PARTS = {".git", ".venv", ".pytest_cache", "__pycache__", "raw"}


def _project_strings_in_json(node, key=None, path="") -> list[tuple[str, str]]:
    """Every string this project wrote in a JSON document, with its path.

    Values reached through a SOURCE_DATA_KEYS key are copied from a source and
    are skipped. Everything else is project prose.
    """
    if key in SOURCE_DATA_KEYS:
        return []
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            out += _project_strings_in_json(v, k, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out += _project_strings_in_json(v, key, f"{path}[{i}]")
    elif isinstance(node, str):
        out.append((path, node))
    return out


def _export_header(text: str) -> str:
    """The comment header of an export. The rows beneath it are source data."""
    return "\n".join(l for l in text.splitlines() if l.startswith("#") or l.startswith("|---"))


def test_no_trend_words_anywhere_in_repo():
    """Whole-word match over this project's own prose, wherever it appears.

    Scoped by key, not by file. This test cannot catch a sentence that implies a
    trend without using a banned word. That gap is covered by the Phase 7 manual
    trend-framing review recorded in governance/safeguards.md.
    """
    import json
    import re

    from conftest import REPO_ROOT

    pattern = re.compile(r"\b(" + "|".join(BANNED_TREND_WORDS) + r")\b", re.I)
    findings = []

    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file() or TREND_SKIP_PARTS & set(path.parts):
            continue
        rel = str(path.relative_to(REPO_ROOT))
        if rel in TREND_BAN_EXEMPT_PATHS or path.suffix not in TREND_SUFFIXES:
            continue

        if path.suffix == ".json":
            try:
                doc = json.loads(path.read_text())
            except ValueError:
                continue
            for where, text in _project_strings_in_json(doc):
                for m in pattern.finditer(text):
                    findings.append(f"{rel} :: {where} :: '{m.group(0)}'")
        elif path.name.startswith("oversight_information_pack"):
            for m in pattern.finditer(_export_header(path.read_text())):
                findings.append(f"{rel} :: export header :: '{m.group(0)}'")
        else:
            for m in pattern.finditer(path.read_text(errors="replace")):
                findings.append(f"{rel} :: '{m.group(0)}'")

    assert not findings, "trend words in this project's own prose:\n" + "\n".join(findings)


def test_crosswalk_caveat_present_verbatim():
    """The crosswalk was dropped, so the caveat must not appear on the site.

    Publishing it would imply an analysis this project does not perform.
    """
    from conftest import REPO_ROOT
    present = [p.name for p in sorted((REPO_ROOT / "docs").glob("*.html"))
               if REQUIRED_CROSSWALK_CAVEAT in p.read_text()]
    assert not present, f"crosswalk caveat published although the analysis was dropped: {present}"
