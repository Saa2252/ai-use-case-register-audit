"""Published figures still match the file they were counted from.

The rest of the suite checks wording, structure and provenance. It does not
check whether a number on a page is the number the data holds. Two were not:
the identifier repeat count read "thirteen" on two pages where the file holds
twelve, and a counting-traps heading said seven above a sentence that said six.
Both were typed by hand rather than computed, which is what S5 exists to stop.

This test recomputes each figure from the raw file and fails if the published
copy has moved away from it. It skips when the raw file is absent, in the same
way as T1 and T7, because raw data is never committed.

Verified by planting the failure: changing any checked figure in the published
data or copy makes this fail and names the figure.
"""

import json
import sys

import pandas as pd
import pytest

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src.measures import _empty_rule, is_empty  # noqa: E402

RAW = REPO_ROOT / "data" / "raw" / "omb2025_individually_reported.csv"
DOCS = REPO_ROOT / "docs"
NINE = [
    "hi_testing_conducted", "hi_assessment_completed", "hi_potential_impacts",
    "hi_independent_review", "hi_ongoing_monitoring", "hi_training_established",
    "hi_failsafe_presence", "hi_appeal_process", "hi_public_consultation",
]


def _register():
    if not RAW.exists():
        pytest.skip("raw data not present: run the acquisition step first")
    return pd.read_csv(RAW, dtype=str, low_memory=False)


def _blank(frame, column):
    always, text_only, types = _empty_rule()
    return frame[column].map(lambda v: is_empty(column, v, always, text_only, types))


def test_published_figures_match_the_raw_file():
    register = _register()
    high = register[register["is_high_impact"] == "High-impact"]
    empty = high[NINE].apply(lambda col: col.map(
        lambda v: is_empty(col.name, v, *_empty_rule()[0:1] + _empty_rule()[1:])))
    ids = register["id"][~_blank(register, "id")].astype(str).str.strip()
    repeats = ids.value_counts()

    expected = {
        "entries": len(register),
        "high_impact": int((register["is_high_impact"] == "High-impact").sum()),
        "classification_not_recorded": int(_blank(register, "is_high_impact").sum()),
        "no_usable_identifier": int(_blank(register, "id").sum()),
        "identifier_values_on_more_than_one_row": int((repeats > 1).sum()),
        "rows_carrying_a_repeated_identifier": int(repeats[repeats > 1].sum()),
        "high_impact_with_no_withholding_status": int(_blank(high, "is_withheld").sum()),
        "oversight_all_nine_empty": int((empty.sum(axis=1) == len(NINE)).sum()),
        "oversight_all_nine_filled": int((empty.sum(axis=1) == 0).sum()),
    }

    findings = json.loads((DOCS / "data" / "findings.json").read_text())
    by_measure = {f["measure"]: f for f in findings["findings"]}
    reuse = json.loads((DOCS / "data" / "reusability_findings.json").read_text())
    r3 = {f["id"]: f for f in reuse["findings"]}["R3"]["figures"]

    published = {
        "entries": by_measure["M2"]["rows"],
        "high_impact": by_measure["M4"]["subset_size"],
        "classification_not_recorded": by_measure["M4"]["bands"]["classification not recorded"],
        "no_usable_identifier": r3["rows_with_no_usable_identifier"],
        "identifier_values_on_more_than_one_row": r3["identifier_values_on_more_than_one_row"],
        "rows_carrying_a_repeated_identifier": r3["rows_carrying_a_repeated_identifier"],
        "high_impact_with_no_withholding_status":
            by_measure["M4"]["withholding_status"]["high_impact_with_no_status"],
        "oversight_all_nine_empty": by_measure["M4"]["oversight_block_shape"]["none_answered"],
        "oversight_all_nine_filled": by_measure["M4"]["oversight_block_shape"]["all_nine_answered"],
    }

    drift = [
        f"{key}: published {published[key]}, the file holds {value}"
        for key, value in expected.items() if published[key] != value
    ]
    assert not drift, "published figures no longer match the file:\n" + "\n".join(drift)


def test_no_page_types_a_figure_the_data_contradicts():
    """The specific words that were wrong, so the same mistake cannot return.

    These are counts the project once wrote out in words instead of computing.
    Each is checked against the file rather than against another page.
    """
    register = _register()
    ids = register["id"][~_blank(register, "id")].astype(str).str.strip()
    repeats = int((ids.value_counts() > 1).sum())
    words = {12: "twelve", 13: "thirteen", 14: "fourteen"}

    wrong = []
    for page in sorted(DOCS.glob("*.html")):
        text = page.read_text().lower()
        for number, word in words.items():
            if number == repeats:
                continue
            if f"{word} identifier values" in text or f"{word} values appear" in text:
                wrong.append(f"{page.name}: says '{word}' where the file holds {repeats}")
    assert not wrong, "a page states an identifier count the file contradicts:\n" + "\n".join(wrong)


def test_the_counting_traps_count_agrees_with_itself():
    """The heading, the sentence under it and the closing summary all say seven."""
    reuse = json.loads((DOCS / "data" / "reusability_findings.json").read_text())
    total = len(reuse["findings"])
    words = {6: "six", 7: "seven", 8: "eight"}
    gaps = (DOCS / "gaps.html").read_text().lower()
    assert f"{words[total]} ways a careful person" in gaps, (
        f"the counting-traps heading does not say {words[total]}, and there are {total} findings")
    wrong = [w for n, w in words.items()
             if n != total and f"these {w} are the reasons" in gaps]
    assert not wrong, (
        f"gaps.html says 'these {wrong[0]} are the reasons' where there are {total} findings")
