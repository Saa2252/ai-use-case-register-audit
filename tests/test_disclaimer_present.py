"""T6. The exact disclaimer appears in every HTML page, the README and every export.

Enforces: S9
See governance/safeguards.md.
"""

import sys

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src.disclaimer import AUTHORSHIP, DISCLAIMER, EXPORT_NOTICE  # noqa: E402

EXPORTS = ["oversight_information_pack.csv", "oversight_information_pack.md"]


def _normalise(text: str) -> str:
    """Export headers prefix each line with a comment marker."""
    return text.replace("# ", "").replace("\n", " ")


def test_disclaimer_on_every_page():
    missing = [p.name for p in sorted((REPO_ROOT / "docs").glob("*.html"))
               if DISCLAIMER not in p.read_text()]
    assert not missing, f"pages with no disclaimer: {missing}"


def test_disclaimer_in_readme():
    assert DISCLAIMER in (REPO_ROOT / "README.md").read_text()


def test_authorship_on_every_page():
    missing = [p.name for p in sorted((REPO_ROOT / "docs").glob("*.html"))
               if AUTHORSHIP not in p.read_text()]
    assert not missing, f"pages with no authorship line: {missing}"


def test_exports_carry_disclaimer_and_notice():
    problems = []
    for name in EXPORTS:
        path = REPO_ROOT / "data" / "derived" / name
        if not path.exists():
            problems.append(f"{name}: missing")
            continue
        text = _normalise(path.read_text())
        if " ".join(DISCLAIMER.split()) not in " ".join(text.split()):
            problems.append(f"{name}: no disclaimer")
        if EXPORT_NOTICE not in text:
            problems.append(f"{name}: no practice-exercise notice")
    assert not problems, problems
