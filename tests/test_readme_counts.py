"""The counts the README states about this repository, checked against it.

The README describes the project to someone who will not run it. A number in
that description is a published figure like any other, and this project has
already found five that were wrong because they were typed rather than counted.

The test count in the README was one of them: it said 30 while the suite held
48. Nothing caught it, because T5 reads HTML and this is Markdown.

Enforces: S5, in the one place S5's own machinery could not reach.
"""

import re
import subprocess
import sys

from conftest import REPO_ROOT

README = REPO_ROOT / "README.md"


def _collected_tests() -> int:
    """How many tests pytest actually collects, asked of pytest itself."""
    out = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=300,
    )
    found = re.search(r"(\d+) tests? collected", out.stdout)
    assert found, "could not read a collected count from pytest:\n" + out.stdout[-600:]
    return int(found.group(1))


def test_the_readme_states_the_real_number_of_tests():
    text = README.read_text(encoding="utf-8")
    stated = re.search(r"\|\s*`tests/`\s*\|\s*([\d,]+)\s+automated checks", text)
    assert stated, "the README no longer states a test count in the form this checks"
    claimed = int(stated.group(1).replace(",", ""))
    actual = _collected_tests()
    assert claimed == actual, (
        f"the README says {claimed} automated checks, the suite collects {actual}"
    )


def test_every_path_the_readme_names_exists():
    """A structure table that names a file which is not there misleads a reader.

    Only paths written in backticks and starting with a known top-level
    directory are checked, so ordinary prose in backticks is not treated as a
    path.
    """
    text = README.read_text(encoding="utf-8")
    roots = ("governance/", "notebooks/", "data/", "docs/", "tests/", "scripts/", "src/")
    missing = []
    for found in re.finditer(r"`([^`]+)`", text):
        candidate = found.group(1).strip()
        if candidate.startswith(roots) and " " not in candidate:
            if not (REPO_ROOT / candidate).exists():
                missing.append(candidate)
    assert not missing, "the README names paths that do not exist: " + ", ".join(sorted(set(missing)))
