"""The register validator runs, finds what the audit found, and leaks nothing.

The audit is a report about one file in one year. The validator is the same
checks as a tool, so next year's file, or another organisation's, can be put
through them without repeating the work.

A tool that reads a register is a new way to break S2. The columns it reads
carry free text written by the people who filed each entry, and that text
carries product and supplier names. A validator that echoed what it found would
publish exactly what the rest of this project removes, and it would do it on
somebody's terminal where no test on `docs/` would ever see it.

Three checks:

1. It runs on the real file and exits cleanly.
2. Nothing it prints is a value out of the file. Every distinct value from the
   free-text columns is searched for in the output.
3. It reproduces findings the audit reached independently, so a check that
   silently stops working is visible.

Skips without raw data, in the same way as T1 and T7.

Verified by planting the failure: printing any value in place of a count fails
the second check and names the column it came from.
"""

import re
import subprocess
import sys

import pytest

from conftest import REPO_ROOT

RAW = REPO_ROOT / "data" / "raw"
REGISTER = RAW / "omb2025_individually_reported.csv"
DICTIONARY = RAW / "omb2025_data_dictionary.json"
SCRIPT = REPO_ROOT / "scripts" / "validate_register.py"

# The columns whose contents are prose written by whoever filed the entry.
FREE_TEXT = ["use_case_name", "problem_solved", "benefits", "system_outputs",
             "data_description", "vendor_name", "system_name_ato"]


def _run() -> str:
    if not REGISTER.exists() or not DICTIONARY.exists():
        pytest.skip("raw data not present: run scripts/acquire.py first")
    out = subprocess.run(
        [sys.executable, str(SCRIPT), str(REGISTER), "--dictionary", str(DICTIONARY)],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=300,
    )
    assert out.returncode == 0, f"the validator exited {out.returncode}:\n{out.stderr[-800:]}"
    return out.stdout


def test_it_runs_on_the_real_file():
    output = _run()
    for heading in ["Does the file open the usual way",
                    "Columns that look answered and are not",
                    "The identifier column",
                    "Columns required only under a condition"]:
        assert heading in output, f"the validator no longer reports: {heading}"


def _expected_vocabulary(register) -> set:
    """Words the validator prints because they are its own, not the file's.

    Two kinds. The placeholder tokens it searches for, which it has to name to
    report them, and the column names, which are the whole point of the output.
    Both happen to occur as values in the file as well. Excluding them keeps
    this test about content rather than coincidence, and they are taken from
    the script itself rather than typed here, so widening the list in the
    script cannot quietly widen what this test permits.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("validate_register", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    vocabulary = {t.lower() for t in module.AMBIGUOUS_PLACEHOLDERS}
    vocabulary |= {t.lower() for t in module.LOOKS_FULL_IS_EMPTY}
    vocabulary |= {c.lower() for c in register.columns}
    return vocabulary


def test_it_prints_no_value_out_of_the_file():
    import pandas as pd
    output = _run().lower()
    register = pd.read_csv(REGISTER, dtype=str, low_memory=False)
    allowed = _expected_vocabulary(register)
    leaked = []
    for column in FREE_TEXT:
        if column not in register.columns:
            continue
        for value in register[column].dropna().astype(str).unique():
            value = value.strip()
            # Very short values are words like "no" that occur in ordinary
            # prose. The check is for content, not for coincidence.
            if len(value) < 12 or value.lower() in allowed:
                continue
            if value.lower() in output:
                leaked.append(f"{column}: a value of {len(value)} characters reached the output")
                break
    assert not leaked, (
        "the validator printed something out of the file. These columns carry supplier and "
        "product names, and this output is not covered by any check on docs/:\n"
        + "\n".join(leaked)
    )


def test_it_finds_what_the_audit_found():
    """Independent arrival at the audit's own figures.

    These are not copied from the findings. The validator computes them from
    the raw file by its own route, so a check that quietly stops working shows
    up here rather than in a report nobody re-reads.
    """
    output = _run()
    found = re.search(r"No identifier at all: (\d+)", output)
    assert found and int(found.group(1)) > 700, (
        "the identifier check no longer reports the missing identifiers the audit found")

    found = re.search(r"(\d+) of \d+ columns carry a condition", output)
    assert found and int(found.group(1)) >= 20, (
        "the conditional-column check no longer finds the conditions that produced two "
        "wrong figures on this site")

    assert "demographic_features" in output and "hi_public_consultation" in output, (
        "the two columns that look answered and are nearly empty are no longer reported")
