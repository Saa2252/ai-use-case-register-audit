"""Compare one register entry against the raw downloaded file, field by field.

Rerun at any time:

    ./.venv/bin/python scripts/verify_entry.py CFTC-003

Prints the raw row exactly as downloaded, the row as published on the site, and
every difference between them with the reason. Nothing here reads the derived
findings: it goes back to the file whose hash is recorded in provenance.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.measures import CORE_FIELDS, _empty_rule, is_empty  # noqa: E402

RAW = REPO_ROOT / "data" / "raw" / "omb2025_individually_reported.csv"
SCRUBBED = REPO_ROOT / "data" / "derived" / "register_2025_scrubbed.csv"
TABLE = REPO_ROOT / "docs" / "data" / "register_table.json"
FULL = REPO_ROOT / "docs" / "data" / "register_full.json"

DROPPED = {
    "vendor_name": "dropped: names a vendor (S2)",
    "system_name_ato": "dropped: may name a product (S2)",
    "contact_email": "dropped: personal data (S8)",
}


def main(entry_id: str) -> int:
    raw = pd.read_csv(RAW, dtype=str, low_memory=False)
    scrubbed = pd.read_csv(SCRUBBED, dtype=str, low_memory=False)
    match = raw.index[raw["id"] == entry_id].tolist()
    if not match:
        print(f"no entry with id {entry_id!r} in the raw file")
        return 1
    i = match[0]

    print("=" * 78)
    print(f"RAW ROW as downloaded, row {i}, from {RAW.name}")
    print("=" * 78)
    for column in raw.columns:
        value = raw.at[i, column]
        shown = "<missing>" if pd.isna(value) else repr(str(value))
        print(f"  {column:<26} {shown[:200]}")

    print()
    print("=" * 78)
    print("FIELD BY FIELD: raw against what the site publishes")
    print("=" * 78)
    full = json.loads(FULL.read_text())
    panel = dict(zip(full["fields"], full["rows"][i]))

    differences = 0
    for column in raw.columns:
        before = "" if pd.isna(raw.at[i, column]) else str(raw.at[i, column])
        if column in DROPPED:
            print(f"  {column:<26} {DROPPED[column]}")
            differences += 1
            continue
        after = panel.get(column)
        if after is None:
            print(f"  {column:<26} NOT IN PANEL  <-- unexpected")
            differences += 1
        elif before != after:
            print(f"  {column:<26} CHANGED")
            print(f"      raw:   {before[:150]!r}")
            print(f"      panel: {after[:150]!r}")
            differences += 1
        else:
            print(f"  {column:<26} identical")

    extra = [f for f in panel if f not in raw.columns]
    for column in extra:
        print(f"  {column:<26} IN PANEL, NOT IN RAW  <-- unexpected")
        differences += 1

    print()
    print(f"  raw columns: {len(raw.columns)}   panel fields: {len(panel)}   "
          f"differences: {differences}")

    print()
    print("=" * 78)
    print("COMPLETENESS: which core fields count as filled for this entry")
    print("=" * 78)
    always, text_only, types = _empty_rule()
    filled = []
    for column in CORE_FIELDS:
        value = scrubbed.at[i, column]
        empty = is_empty(column, value, always, text_only, types)
        shown = "<missing>" if pd.isna(value) else repr(str(value))[:70]
        print(f"  {'FILLED ' if not empty else 'empty  '} {column:<26} {shown}")
        if not empty:
            filled.append(column)
    table = json.loads(TABLE.read_text())
    print()
    print(f"  filled: {len(filled)} of {len(CORE_FIELDS)} core fields "
          f"= {round(len(filled) / len(CORE_FIELDS) * 100)}%")
    print(f"  the table published for this row says: {table['rows'][i]['n']} of "
          f"{table['core_fields']}")
    print(f"  agreement: {len(filled) == table['rows'][i]['n']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "CFTC-003"))
