"""T10. Every finding in derived JSON carries a non-empty caveat field.

Enforces: M2, M4
See governance/safeguards.md.
"""

import json

import pytest

from conftest import REPO_ROOT

FINDINGS = REPO_ROOT / "data" / "derived" / "findings.json"


def test_every_finding_has_a_caveat():
    if not FINDINGS.exists():
        pytest.skip("findings.json not written yet: run the Phase 5 analysis first")
    data = json.loads(FINDINGS.read_text())
    missing = [f.get("measure", "?") for f in data["findings"]
               if not str(f.get("caveat", "")).strip()]
    assert not missing, f"findings with no caveat: {missing}"


def test_findings_carry_the_rule_applied():
    if not FINDINGS.exists():
        pytest.skip("findings.json not written yet")
    data = json.loads(FINDINGS.read_text())
    missing = [f.get("measure", "?") for f in data["findings"]
               if not str(f.get("rule_applied", "")).strip()]
    assert not missing, f"findings with no rule recorded: {missing}"
