"""Build the oversight information pack, the M4 export.

The notebook named this script in a comment and the script was not there. The
two committed export files could not be rebuilt by anyone following the
README, which tells a reader to run the notebook to reproduce the work. Writing
it here puts the export where it can be run and tested, and the notebook calls
it rather than restating it.

Two things changed when it was written.

The disclaimer in the header now names the UK source, which the owner added on
2026-09-30.

The nine oversight columns no longer answer "no" for every entry. The register
asks them only of high-impact entries that are deployed, and a pack that
answers "no" on a pre-deployment entry hands an oversight body a negative
answer to a question nobody asked. Those cells now read "not asked", and the
count of fields provided is reported only where the register asks.

Run:  python scripts/build_export.py
"""

import sys
import warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
warnings.filterwarnings("ignore")

import pandas as pd  # noqa: E402

from src import conditionality as COND  # noqa: E402
from src.disclaimer import AUTHORSHIP, DISCLAIMER, EXPORT_NOTICE  # noqa: E402
from src.measures import _empty_rule, is_empty, oversight_fields  # noqa: E402

DERIVED = REPO_ROOT / "data" / "derived"
DOCS_DATA = REPO_ROOT / "docs" / "data"

TITLE = "Oversight information pack"
IDENTITY = ["id", "agency_name", "agency_bureau", "use_case_name",
            "development_stage", "is_high_impact"]

READING = (
    "A field marked yes shows that information was provided. It does not show that the practice\n"
    "described is adequate. A field marked no is not evidence that the practice is absent."
)
CONDITION_NOTE = (
    "The register asks these nine questions only of high-impact use cases that are deployed.\n"
    "A field marked not asked is one the register does not put to that entry, which is a\n"
    "different fact from an answer of no. An earlier version of this pack answered no in those\n"
    "cells. See governance/corrections.md."
)

ASKED, NOT_ASKED, PROVIDED, NOT_PROVIDED = "asked", "not asked", "yes", "no"


def build() -> pd.DataFrame:
    register = pd.read_csv(DERIVED / "register_2025_scrubbed.csv", dtype=str, low_memory=False)
    always, text_only, types = _empty_rule()
    nine = oversight_fields(register.columns)
    high_impact = register[register["is_high_impact"] == "High-impact"]

    asked, _ = COND.asked_of(register, nine[0])
    asked = asked.loc[high_impact.index]

    out = high_impact[IDENTITY].copy()
    out.insert(len(IDENTITY), "register_asks_the_nine",
               asked.map(lambda yes: ASKED if yes else NOT_ASKED))

    filled = pd.Series(0, index=high_impact.index)
    for field in nine:
        has_value = ~high_impact[field].map(
            lambda v, f=field: is_empty(f, v, always, text_only, types))
        filled = filled + has_value.astype(int)
        out[field + "_provided"] = [
            (PROVIDED if value else NOT_PROVIDED) if is_asked else NOT_ASKED
            for value, is_asked in zip(has_value, asked)
        ]
    out.insert(len(IDENTITY) + 1, "oversight_fields_provided",
               [str(int(n)) if is_asked else NOT_ASKED for n, is_asked in zip(filled, asked)])
    return out.fillna("")


def header_lines(rows: int, asked_rows: int) -> list[str]:
    return [
        TITLE,
        "",
        EXPORT_NOTICE,
        "",
        DISCLAIMER,
        "",
        AUTHORSHIP,
        "",
        f"Entries flagged high-impact in the published data: {rows}",
        f"Of those, entries the register asks the nine oversight questions of: {asked_rows}",
        "",
        READING,
        "",
        CONDITION_NOTE,
    ]


def write_markdown(table: pd.DataFrame, path: Path, header: list[str]) -> None:
    lines = ["# " + header[0]] + header[1:]
    body = ["| " + " | ".join(table.columns) + " |",
            "|" + "---|" * len(table.columns)]
    for row in table.itertuples(index=False):
        body.append("| " + " | ".join(str(v).replace("|", "/") for v in row) + " |")
    path.write_text("\n".join(lines + [""] + body) + "\n", encoding="utf-8")


def write_csv(table: pd.DataFrame, path: Path, header: list[str]) -> None:
    prefix = "\n".join(("# " + line).rstrip() for line in header)
    path.write_text(prefix + "\n\n" + table.to_csv(index=False), encoding="utf-8")


def main() -> int:
    table = build()
    asked_rows = int((table["register_asks_the_nine"] == ASKED).sum())
    header = header_lines(len(table), asked_rows)
    for directory in (DERIVED, DOCS_DATA):
        directory.mkdir(parents=True, exist_ok=True)
        write_markdown(table, directory / "oversight_information_pack.md", header)
        write_csv(table, directory / "oversight_information_pack.csv", header)
    print(f"rows: {len(table)}  asked the nine: {asked_rows}  "
          f"not asked: {len(table) - asked_rows}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
