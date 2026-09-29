"""T5. HTML files contain no numbers of three or more digits outside the disclaimer and dates.

Enforces: S5
See governance/safeguards.md.

Every figure on the site is injected at load time from docs/data. A three-digit
number written into the markup would be a number nobody can trace back to the
notebook.
"""

import re
import sys

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src.disclaimer import DISCLAIMER, ONTARIO_ATTRIBUTION, REPOSITORY_URL  # noqa: E402

YEAR = re.compile(r"^(19|20)\d{2}$")


def test_no_hardcoded_numbers_in_html():
    findings = []
    for path in sorted((REPO_ROOT / "docs").glob("*.html")):
        text = path.read_text()
        text = text.replace(DISCLAIMER, " ").replace(ONTARIO_ATTRIBUTION, " ")
        # Exact-string exemption approved by the owner on 30 September 2026: the
        # repository address carries digits inside the account name. Blanking the
        # exact address leaves every other number in the page checked, including
        # any that appears next to the link. While the address is empty, nothing
        # is blanked. See governance/safeguards.md.
        if REPOSITORY_URL:
            text = text.replace(REPOSITORY_URL, " " * len(REPOSITORY_URL))
        for m in re.finditer(r"\d{3,}", text):
            if YEAR.match(m.group(0)):
                continue
            line = text[:m.start()].count("\n") + 1
            findings.append(f"{path.name}:{line} '{m.group(0)}'")
    assert not findings, "numbers written into HTML instead of loaded from data:\n" + "\n".join(findings)
