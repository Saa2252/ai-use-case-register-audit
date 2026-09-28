"""T7. Raw file SHA-256 hashes match the recorded manifest.

Enforces: S7
See governance/safeguards.md.

Raw files are downloaded, hashed and then read only. If a hash no longer
matches, a file has been edited and every finding downstream is suspect.
"""

import json
import sys

import pytest

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src.provenance import sha256_of  # noqa: E402

MANIFEST = REPO_ROOT / "data" / "raw" / "manifest.json"


def test_raw_file_hashes_match_provenance():
    if not MANIFEST.exists():
        pytest.skip("raw manifest not present: run the Phase 1 download first")
    problems = []
    for entry in json.loads(MANIFEST.read_text()):
        path = REPO_ROOT / "data" / "raw" / entry["local_name"]
        if not path.exists():
            problems.append(f"missing: {entry['local_name']}")
        elif sha256_of(path) != entry["sha256"]:
            problems.append(f"hash changed: {entry['local_name']}")
    assert not problems, "raw data no longer matches what was downloaded:\n" + "\n".join(problems)
