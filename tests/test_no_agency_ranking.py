"""T3. No derived file or page contains per-agency scores, ranks or sorted comparisons.

Enforces: S3
See governance/safeguards.md.

Agency names may appear as published facts in row-level detail. What may not
appear is any construct that ranks, scores or orders agencies against each
other.
"""

import json
import re

from conftest import REPO_ROOT

RANKING_WORDS = [r"\brank(ed|ing|s)?\b", r"\bleague table\b", r"\btop\s+\d+\b",
                 r"\bbest\b", r"\bworst\b", r"\bleader ?board\b", r"\bscorecard\b",
                 r"\bbetter than\b", r"\bcompared with other agencies\b"]


def test_no_ranking_language_on_site():
    found = []
    for path in sorted((REPO_ROOT / "docs").glob("*.html")):
        text = path.read_text()
        for pat in RANKING_WORDS:
            for m in re.finditer(pat, text, re.I):
                found.append(f"{path.name}: '{m.group(0)}'")
    assert not found, f"ranking language on the site: {found}"


def test_findings_carry_no_per_agency_figures():
    """No finding may publish a figure broken down by agency."""
    path = REPO_ROOT / "data" / "derived" / "findings.json"
    if not path.exists():
        return
    agencies = set()
    table = REPO_ROOT / "docs" / "data" / "register_table.json"
    if table.exists():
        agencies = {r["a"] for r in json.loads(table.read_text())["rows"]}
    blob = path.read_text()
    named = sorted(a for a in agencies if a and a in blob)
    assert not named, f"findings.json names individual agencies: {named[:5]}"
