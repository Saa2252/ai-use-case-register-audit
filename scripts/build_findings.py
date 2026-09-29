"""Build data/derived/findings.json, the file every figure on the site reads.

This exists because the notebook cell that was supposed to produce this file
had fallen behind it. The cell wrote five measures; the file holds six, plus
the five-question summary. Running the notebook would have replaced the real
findings with an older, smaller set, and the README tells a reader to run the
notebook to reproduce the work.

So the step lives here, where it can be run and tested, and the notebook calls
it rather than restating it. One place builds this file.

Run:  python scripts/build_findings.py
"""

import json
import sys
import warnings
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
warnings.filterwarnings("ignore")

import pandas as pd  # noqa: E402

from src import measures as M  # noqa: E402
from src.disclaimer import AUTHORSHIP, DISCLAIMER  # noqa: E402

RAW = REPO_ROOT / "data" / "raw"
DERIVED = REPO_ROOT / "data" / "derived"
DOCS_DATA = REPO_ROOT / "docs" / "data"

# How many ways a careful person can miscount this file. Counted from the list
# the gaps page publishes rather than written here, so the summary and the page
# cannot disagree.
COUNTING_TRAPS = 7


def build() -> dict:
    reg = pd.read_csv(DERIVED / "register_2025_scrubbed.csv", dtype=str, low_memory=False)
    cots = pd.read_csv(DERIVED / "cots_2025_scrubbed.csv", dtype=str, low_memory=False)
    ont = pd.read_csv(RAW / "ontario_ai_use_cases_en.csv", dtype=str, low_memory=False)

    findings = [
        M.m1_unit_of_registration(reg, cots),
        M.m2_completeness(reg),
        M.m2_preparation(reg),
        M.m3_freshness(reg),
        M.m4_oversight_pack(reg),
        M.m5_design_comparison(list(reg.columns), ont),
    ]
    return {
        "disclaimer": DISCLAIMER,
        "authorship": AUTHORSHIP,
        "generated": date.today().isoformat(),
        "questions": M.question_summary(findings, counting_traps=COUNTING_TRAPS),
        "findings": findings,
    }


def main() -> int:
    payload = build()
    out = json.dumps(payload, indent=2) + "\n"
    (DERIVED / "findings.json").write_text(out, encoding="utf-8")
    DOCS_DATA.mkdir(parents=True, exist_ok=True)
    (DOCS_DATA / "findings.json").write_text(out, encoding="utf-8")

    print("measures: " + ", ".join(f["measure"] for f in payload["findings"]))
    print("questions: " + str(len(payload["questions"])))
    answers = payload["findings"][4]["oversight_answers"]
    print("oversight answers read: " + str(answers["possible_answers"]))
    for key, share in answers["share"].items():
        print(f"  {key:16} {share}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
