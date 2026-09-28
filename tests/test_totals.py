"""T1. Row counts in raw files match the expected totals recorded in provenance.

Enforces: S6
See governance/safeguards.md.
"""

import csv
import json

import pytest

from conftest import REPO_ROOT

RAW = REPO_ROOT / "data" / "raw"

EXPECTED = {
    "omb2025_individually_reported.csv": 3611,
    "omb2025_consolidated_cots.csv": 900,
    "omb2024_inventory_v2.csv": 2133,
    "ontario_ai_use_cases_en.csv": 3,
}

ENCODINGS = {"omb2024_inventory_v2.csv": "cp1252"}


def _rows(path, encoding="utf-8"):
    with path.open(newline="", encoding=encoding) as fh:
        return sum(1 for _ in csv.reader(fh)) - 1


def test_row_counts_match_published_totals():
    if not (RAW / "manifest.json").exists():
        pytest.skip("raw data not present: run the Phase 1 download first")
    problems = []
    for name, expected in EXPECTED.items():
        path = RAW / name
        if not path.exists():
            problems.append(f"{name}: missing")
            continue
        observed = _rows(path, ENCODINGS.get(name, "utf-8"))
        if observed != expected:
            problems.append(f"{name}: expected {expected:,}, found {observed:,}")
    assert not problems, "row counts no longer match:\n" + "\n".join(problems)
