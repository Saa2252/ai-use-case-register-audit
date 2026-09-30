"""Which entries the register actually asks each question of.

The publisher's dictionary states a Required clause for every field, and most
of them carry a condition. Twenty of the thirty-five say Required: Yes followed
by a limit, such as "for pilot and deployed use cases" or "only for high-impact
deployed use cases". A field with a condition is not asked of every entry, so a
blank in it on an entry outside the condition records that the question was not
put, not that it was left unanswered.

This project counted one set of those fields across the wrong population and
published the figure. The correction covered the nine oversight fields. It did
not cover the rest, because nothing in the analysis read the Required clause.
This module reads it, for every field, from the dictionary itself.

Three answers are possible for each entry and each field, and the third one
matters:

  asked          the entry meets the condition
  not asked      the entry does not meet it
  undetermined   the field the condition depends on is blank on that entry

338 entries carry no development stage. For any field conditioned on stage,
those entries cannot be placed on either side, and a count that quietly puts
them on one side states something the file does not contain.

Parsing is deliberately strict. An unrecognised Required clause raises rather
than falling back to "asked of everything", because falling back is exactly the
assumption that produced the original defect.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW = REPO_ROOT / "data" / "raw"
DICTIONARY = RAW / "omb2025_data_dictionary.json"

# The stage values as the scrubbed register holds them, mapped from the words
# the Required clauses use. The clauses are prose and the column is a category,
# so the join between them is written down here rather than guessed at.
STAGE_WORDS = {
    "pre-deployment": "Pre-deployment",
    "pilot": "Pilot",
    "deployed": "Deployed",
    "retired": "Retired",
}

HIGH_IMPACT_VALUE = "High-impact"
PRESUMED_NOT_HIGH_IMPACT = "Presumed High-Impact, but Not High-impact"


def _dictionary() -> dict:
    return json.loads(DICTIONARY.read_text(encoding="utf-8"))


def required_clause(field: str, dictionary: dict | None = None) -> str:
    """The Required sentence for a field, verbatim from the dictionary."""
    dictionary = dictionary or _dictionary()
    instructions = (dictionary.get(field, {}).get("instructions") or "")
    found = re.search(r"Required:\s*(.*)$", instructions, re.S)
    return " ".join(found.group(1).split()) if found else ""


def condition(field: str, dictionary: dict | None = None) -> dict:
    """What the Required clause says, as something the analysis can apply.

    Raises on a clause this has not been taught to read. A field whose
    condition is unknown must stop the build, not default to being asked of
    every entry.
    """
    clause = required_clause(field, dictionary)
    plain = clause.lower().rstrip(".")

    if not clause:
        return {"kind": "not_stated", "clause": clause}
    if plain == "yes":
        return {"kind": "always", "clause": clause}
    if plain == "no":
        return {"kind": "optional", "clause": clause}
    if plain == "yes, only for high-impact deployed use cases":
        return {"kind": "high_impact_and_stage", "stages": ["Deployed"], "clause": clause}

    stages = re.fullmatch(r"yes, for (.+?) use cases", plain)
    if stages:
        words = re.split(r",| and ", stages.group(1))
        wanted = []
        for word in words:
            word = word.strip()
            if not word:
                continue
            if word not in STAGE_WORDS:
                raise ValueError(f"{field}: unreadable stage '{word}' in Required clause")
            wanted.append(STAGE_WORDS[word])
        return {"kind": "stage", "stages": wanted, "clause": clause}

    if plain.startswith("yes, but question should only appear if"):
        return {"kind": "answer", "clause": clause}

    raise ValueError(f"{field}: Required clause not understood: {clause!r}")


# Fields whose condition depends on another field's answer, written out because
# the dictionary states them in prose. Only fields the scrubbed register still
# holds are here. Each returns the mask of entries the question is put to, and
# the mask of entries where the governing answer is blank so it cannot be told.
ANSWER_CONDITIONS = {
    "HI_justification": lambda reg: (
        reg["is_high_impact"].fillna("").str.strip() == PRESUMED_NOT_HIGH_IMPACT,
        reg["is_high_impact"].fillna("").str.strip() == "",
    ),
}


def asked_of(reg: pd.DataFrame, field: str,
             dictionary: dict | None = None) -> tuple[pd.Series, pd.Series]:
    """Which entries the register puts this question to.

    Returns (asked, undetermined). An entry counted as undetermined is in
    neither of the other two groups, and every figure built on this reports it
    rather than folding it into one side.
    """
    rule = condition(field, dictionary)
    stage = reg["development_stage"].fillna("").str.strip()
    no_stage = stage == ""

    if rule["kind"] in {"always", "optional", "not_stated"}:
        return pd.Series(True, index=reg.index), pd.Series(False, index=reg.index)

    if rule["kind"] == "stage":
        return stage.isin(rule["stages"]), no_stage

    if rule["kind"] == "high_impact_and_stage":
        flag = reg["is_high_impact"].fillna("").str.strip()
        asked = (flag == HIGH_IMPACT_VALUE) & stage.isin(rule["stages"])
        # An entry with no classification and no stage cannot be placed. One
        # with a classification of "not high-impact" can: it is not asked.
        return asked, (flag == "") | (no_stage & (flag == HIGH_IMPACT_VALUE))

    if rule["kind"] == "answer":
        builder = ANSWER_CONDITIONS.get(field)
        if builder is None:
            raise ValueError(
                f"{field}: its condition depends on another answer and no rule is written "
                "for it. Write one or drop the field from the figures.")
        return builder(reg)

    raise ValueError(f"{field}: condition kind {rule['kind']!r} has no rule")


def conditional_fields(columns: list[str], dictionary: dict | None = None) -> list[str]:
    """Every field in the register that carries a condition."""
    dictionary = dictionary or _dictionary()
    return [c for c in columns
            if c in dictionary and condition(c, dictionary)["kind"] not in
            {"always", "optional", "not_stated"}]
