"""Check a use case register for the counting problems this project found.

This audit found seven ways a careful person reading the 2025 US federal
register in a spreadsheet would get a wrong answer and not be told. Six of the
seven are properties of the file's contents and can be checked on any file of
the same shape. This runs those checks, so next year's file, or another
organisation's, can be put through them without repeating the audit.

    python scripts/validate_register.py data/raw/omb2025_individually_reported.csv

Add the publisher's data dictionary to get the conditional-denominator check,
which is the one that produced two wrong figures on this site:

    python scripts/validate_register.py <file.csv> --dictionary <dictionary.json>

**It prints counts and field names. It never prints a value.** The fields it
reads carry free text written by the people who filed each entry, and that text
carries product and supplier names. A validator that echoed what it found would
leak exactly what this project removes. Where a value has to be characterised,
it is characterised by shape.

Exit status is 0 when the file is readable, whatever the checks find. A file
with counting problems is the normal case, not a failure of this script.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import pandas as pd  # noqa: E402

# An empty answer stored as something a spreadsheet counts as an answer. The
# first is a pair of brackets with nothing between them, which is what a
# tick-none produces in a multiple-choice field.
LOOKS_FULL_IS_EMPTY = ["[]", "{}", "()", '""', "''", "[ ]"]

# Words that record an absence in one field and a real answer in another. The
# point of the check is not that these are wrong, but that one word cannot be
# read the same way everywhere.
AMBIGUOUS_PLACEHOLDERS = [
    "n/a", "na", "none", "not applicable", "tbd", "to be determined",
    "unknown", "not available", "pending", "-", "--",
]

# A date whose day and month could be swapped. Any value matching this has two
# readings and the file does not say which.
AMBIGUOUS_DATE = re.compile(r"^\s*(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})\s*$")


def _report(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


def check_encoding(path: Path) -> None:
    _report("1. Does the file open the usual way")
    try:
        path.read_text(encoding="utf-8")
        print("   UTF-8: yes. It opens with the default settings.")
    except UnicodeDecodeError as problem:
        print(f"   UTF-8: no. It stops at byte {problem.start}.")
        print("   Anyone reading this file with default settings gets an error, not data.")
        for fallback in ("cp1252", "latin-1"):
            try:
                path.read_text(encoding=fallback)
                print(f"   It decodes as {fallback}. State that wherever the file is published.")
                break
            except UnicodeDecodeError:
                continue


def check_full_looking_empties(df: pd.DataFrame) -> None:
    _report("2. Columns that look answered and are not")
    found = False
    for column in df.columns:
        values = df[column].astype(str).str.strip()
        hits = values.isin(LOOKS_FULL_IS_EMPTY).sum()
        if hits:
            found = True
            share = round(hits / len(df) * 100, 1)
            print(f"   {column}: {hits} of {len(df)} rows ({share}%) hold a value that means "
                  "nothing was ticked.")
    if not found:
        print("   None found.")
    else:
        print("   A spreadsheet counts these as answers. Any completeness figure taken from "
              "this file without treating them as empty reads the column as fuller than it is.")


def check_placeholders(df: pd.DataFrame) -> None:
    _report("3. The same word meaning different things in different columns")
    where = {}
    for column in df.columns:
        values = df[column].astype(str).str.strip().str.lower()
        for token in AMBIGUOUS_PLACEHOLDERS:
            hits = int((values == token).sum())
            if hits:
                where.setdefault(token, []).append((column, hits))
    if not where:
        print("   None found.")
        return
    for token, places in sorted(where.items(), key=lambda kv: -len(kv[1])):
        if len(places) > 1:
            names = ", ".join(f"{c} ({n})" for c, n in places)
            print(f'   "{token}" appears in {len(places)} columns: {names}')
    print("   Where one of these appears in more than one column, decide per column whether "
          "it records an absence or an answer. It cannot be both.")


def check_identifiers(df: pd.DataFrame, column: str) -> None:
    _report(f"4. The identifier column ({column})")
    if column not in df.columns:
        print(f"   No column named {column}. Pass --id-column to name it.")
        return
    values = df[column].astype(str).str.strip()
    blank = int(values.isin(["", "nan", "None"]).sum())
    placeholder = int(values.str.lower().isin(AMBIGUOUS_PLACEHOLDERS).sum())
    usable = values[~values.isin(["", "nan", "None"])
                    & ~values.str.lower().isin(AMBIGUOUS_PLACEHOLDERS)]
    repeats = Counter(usable)
    repeated = {v: c for v, c in repeats.items() if c > 1}
    print(f"   Rows: {len(df)}")
    print(f"   No identifier at all: {blank}")
    print(f"   A placeholder instead of an identifier: {placeholder}")
    print(f"   Identifier values appearing on more than one row: {len(repeated)}, "
          f"covering {sum(repeated.values())} rows")
    if blank or placeholder or repeated:
        print("   Without a unique identifier that stays the same between years, no entry "
              "can be followed from one year to the next.")


def check_dates(df: pd.DataFrame, columns: list[str]) -> None:
    _report("5. Dates that could mean two different days")
    for column in columns:
        if column not in df.columns:
            continue
        values = df[column].astype(str).str.strip()
        present = values[~values.isin(["", "nan", "None"])]
        ambiguous = 0
        for value in present:
            found = AMBIGUOUS_DATE.match(value)
            if found and int(found.group(1)) <= 12 and int(found.group(2)) <= 12:
                ambiguous += 1
        print(f"   {column}: {len(present)} values, {ambiguous} could be read two ways "
              f"({round(ambiguous / len(present) * 100, 1) if len(present) else 0}%)")
    print("   A value where both numbers are twelve or less has two readings and the file "
          "does not say which. Choosing one invents a precision the file does not have.")


def check_conditional_denominators(df: pd.DataFrame, dictionary: dict) -> None:
    _report("6. Columns required only under a condition")
    from src import conditionality as COND

    conditional = []
    for column in df.columns:
        if column not in dictionary:
            continue
        try:
            rule = COND.condition(column, dictionary)
        except ValueError as problem:
            print(f"   {column}: the Required clause could not be read. {problem}")
            continue
        if rule["kind"] in {"always", "optional", "not_stated"}:
            continue
        conditional.append((column, rule))

    if not conditional:
        print("   None. Every column is asked of every entry.")
        return

    print(f"   {len(conditional)} of {len(dictionary)} columns carry a condition.")
    print("   A share of all rows for one of these counts entries the question was never")
    print("   put to. This is the check that produced two wrong figures on this project's")
    print("   own site before it was written.")
    print()
    print(f"   {'column':28} {'asked of':>9} {'not asked':>10} {'undetermined':>13}")
    for column, _ in conditional:
        try:
            asked, undetermined = COND.asked_of(df, column, dictionary)
        except ValueError:
            # Its condition depends on another field's answer, and the rule for
            # reading that answer is written per field. Saying so is the honest
            # output: the column is conditional and this cannot say how many.
            print(f"   {column:28} {'conditional on another answer, not counted':>34}")
            continue
        except KeyError as missing:
            print(f"   {column:28} needs a column this file does not have: {missing}")
            continue
        asked_n, undet_n = int(asked.sum()), int(undetermined.sum())
        print(f"   {column:28} {asked_n:>9} {len(df) - asked_n - undet_n:>10} {undet_n:>13}")
    print()
    print("   Undetermined means the column the condition depends on is itself blank on")
    print("   those rows. They belong in neither group and putting them in one asserts")
    print("   something the file does not hold.")


def check_undocumented_values(df: pd.DataFrame, dictionary: dict) -> None:
    _report("7. Values the file uses and the dictionary does not define")
    found = False
    for column, spec in dictionary.items():
        mapping = spec.get("recoding_map")
        if not mapping or column not in df.columns:
            continue
        # The map is written canonical form -> the ways agencies wrote it. The
        # file holds the written forms, so both sides of the map count as
        # documented. Comparing against the keys alone reports almost every row
        # as undocumented, which is a wrong answer delivered confidently.
        allowed = {str(k).strip().lower() for k in mapping}
        for variants in mapping.values():
            for variant in (variants or []):
                allowed.add(str(variant).strip().lower())
        values = df[column].astype(str).str.strip()
        present = {v for v in values[~values.isin(["", "nan", "None"])]}
        undocumented = {v for v in present if v.lower() not in allowed}
        if undocumented:
            found = True
            rows = int(values.isin(list(undocumented)).sum())
            print(f"   {column}: {len(undocumented)} value(s) not in the dictionary, "
                  f"on {rows} rows.")
    if not found:
        print("   None found.")
    else:
        print("   A reader counting categories from the dictionary will miss these rows.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("file", type=Path, help="the register, as CSV")
    parser.add_argument("--dictionary", type=Path, default=None,
                        help="the publisher's data dictionary, as JSON")
    parser.add_argument("--id-column", default="id", help="the identifier column")
    parser.add_argument("--date-columns", default="operational_date",
                        help="comma-separated date columns")
    args = parser.parse_args()

    if not args.file.exists():
        print(f"no such file: {args.file}")
        return 2

    print("=" * 72)
    print(f"Register check: {args.file.name}")
    print("Counts and column names only. No value from the file is printed.")
    print("=" * 72)

    check_encoding(args.file)
    try:
        df = pd.read_csv(args.file, dtype=str, low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(args.file, dtype=str, low_memory=False, encoding="cp1252")
        print("   Read with cp1252 for the checks below.")

    check_full_looking_empties(df)
    check_placeholders(df)
    check_identifiers(df, args.id_column)
    check_dates(df, [c.strip() for c in args.date_columns.split(",") if c.strip()])

    if args.dictionary and args.dictionary.exists():
        dictionary = json.loads(args.dictionary.read_text(encoding="utf-8"))
        check_conditional_denominators(df, dictionary)
        check_undocumented_values(df, dictionary)
    else:
        _report("6 and 7. Skipped")
        print("   Both need the publisher's data dictionary. Pass --dictionary.")

    print()
    print("=" * 72)
    print("Nothing here says an organisation did anything wrong. Every check describes")
    print("how the file is written, which is a property of the file and not of anyone.")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
