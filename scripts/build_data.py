"""Publish the data the site needs, from the single source of each rule.

Everything here is derived from one place:
  - which fields count towards completeness comes from src.measures.CORE_FIELDS
  - what counts as an empty value comes from data/raw/empty_value_rule.json
  - field types come from the source's own data dictionary

Nothing in docs/ restates a rule. A second copy of a rule drifts, and the drift
is invisible until someone checks one entry by hand.
"""

import json
import sys
import warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
warnings.filterwarnings("ignore")

import pandas as pd  # noqa: E402

from src.labels import FIELD_GROUPS, FIELD_LABELS, GROUP_OF  # noqa: E402
from src.measures import CORE_FIELDS, _empty_rule, is_empty  # noqa: E402

DERIVED = REPO_ROOT / "data" / "derived"
DOCS_DATA = REPO_ROOT / "docs" / "data"
RAW = REPO_ROOT / "data" / "raw"


def main() -> None:
    DOCS_DATA.mkdir(parents=True, exist_ok=True)
    register = pd.read_csv(DERIVED / "register_2025_scrubbed.csv", dtype=str, low_memory=False)
    always, text_only, types = _empty_rule()

    # The rule itself, published so the page applies it rather than restating it.
    rule = json.loads((RAW / "empty_value_rule.json").read_text())
    rule["field_types"] = {c: types.get(c, "free_text") for c in register.columns}
    rule["core_fields"] = CORE_FIELDS
    (DOCS_DATA / "empty_value_rule.json").write_text(json.dumps(rule, indent=1))

    # How many identifier values sit on more than one row. This was typed into
    # two pages as "thirteen" and the file says twelve, so it is computed here
    # and read from the published findings by both. tests/test_published_claims.py
    # recomputes it and fails if either page drifts again.
    for path in (DERIVED / "reusability_findings.json", DOCS_DATA / "reusability_findings.json"):
        if not path.exists():
            continue
        payload = json.loads(path.read_text())
        ids = register["id"][~register["id"].map(
            lambda v: is_empty("id", v, always, text_only, types))].astype(str).str.strip()
        counts = ids.value_counts()
        for finding in payload.get("findings", []):
            if finding.get("id") == "R3":
                finding.setdefault("figures", {})
                finding["figures"]["identifier_values_on_more_than_one_row"] = int((counts > 1).sum())
                finding["figures"]["rows_carrying_a_repeated_identifier"] = int(counts[counts > 1].sum())
        path.write_text(json.dumps(payload, indent=1))

    # Reader-facing labels for the register's own column names, published so the
    # pages never render a raw column name.
    (DOCS_DATA / "field_labels.json").write_text(json.dumps(
        {"labels": FIELD_LABELS, "groups": FIELD_GROUPS, "group_of": GROUP_OF}, indent=1))

    rows = []
    for _, record in register.iterrows():
        filled = sum(
            0 if is_empty(c, record[c], always, text_only, types) else 1 for c in CORE_FIELDS
        )
        rows.append({
            "n": filled,
            "a": record["agency_name"],
            "u": "" if pd.isna(record["use_case_name"]) else str(record["use_case_name"])[:160],
            "s": "" if is_empty("development_stage", record["development_stage"],
                                always, text_only, types) else str(record["development_stage"]),
            "h": "" if pd.isna(record["is_high_impact"]) else str(record["is_high_impact"]),
            "i": "" if is_empty("id", record["id"], always, text_only, types) else str(record["id"]),
        })
    (DOCS_DATA / "register_table.json").write_text(
        json.dumps({"core_fields": len(CORE_FIELDS), "rows": rows}, separators=(",", ":")))

    full = [[("" if pd.isna(v) else str(v)) for v in rec]
            for rec in register.itertuples(index=False, name=None)]
    (DOCS_DATA / "register_full.json").write_text(
        json.dumps({"fields": list(register.columns), "rows": full}, separators=(",", ":")))

    print(f"register_table.json: {len(rows):,} rows, {len(CORE_FIELDS)} core fields")
    print(f"register_full.json: {len(full):,} rows, {len(register.columns)} fields")
    print(f"empty_value_rule.json: {len(rule['empty_always'])} values, published for the page")
    print(f"field_labels.json: {len(FIELD_LABELS)} labels, {len(FIELD_GROUPS)} groups")


if __name__ == "__main__":
    main()
