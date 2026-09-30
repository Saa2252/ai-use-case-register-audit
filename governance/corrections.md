# Corrections

Figures this project published and later changed, and what was done about each.

A correction that only reaches the file is not a correction. The wrong number
was on a public page and was read there, so the note saying it changed goes on
the same page, near the top, for as long as the owner decides. This file is the
permanent record and does not expire.

The wording of each published note is held in `src/corrections.py`. The numbers
inside it are resolved from `data/derived/findings.json` at build time, like
every other number on this site, so a correction cannot itself go stale.

---

## 1. The nine oversight fields, counted against the wrong population

| | |
|---|---|
| Found | 2026-09-30 |
| Corrected in the analysis | 2026-09-30 |
| Correction published | 2026-10-01 |
| Published as | 317 of the 445 entries marked high-impact have none of the nine answered |
| Now published as | 101 of the 227 entries the register asks, which is 44.5% of them |
| Where it ran | `index.html` and `register.html` |
| Note visible on | `index.html`, `register.html` |

**What was wrong.** The publisher's dictionary states of each of the nine
oversight fields: *"Required: Yes, only for high-impact deployed use cases"*.
This project counted blanks across all 445 entries marked high-impact. 218 of
those are at the pre-deployment, pilot or retired stage, and the register does
not put the nine to them. Their blanks record a question that was not asked.

**What it changes.** The gap is smaller and it is still there. On 101 of the
227 entries the register does ask, all nine are blank.

**Why it was not caught.** The condition is written in the dictionary and the
analysis never read it. Every figure in this project was checked against the
data file and none was checked against the statement of who the question is
put to.

---

## 2. The one date field, counted against the wrong population

| | |
|---|---|
| Found | 2026-10-01, during the check below |
| Corrected and published | 2026-10-01 |
| Published as | usable dates cover 31.7% of the register |
| Now published as | usable dates cover 67.6% of the 1,480 entries the register asks |
| Where it ran | `gaps.html`, and the evidence strip on `index.html` |
| Note visible on | `gaps.html`, beside the figure |

**What was wrong.** The dictionary states *"Required: Yes, for pilot and
deployed use cases."* for `operational_date`. Every share published for it
divided by all 3,611 rows.

**What it changes.** The finding does not change. The register still records no
date of verification, no date of update and no date of review, and its one date
field answers a different question. What changes is how empty that field looks:
a third of the entries the register asks still carry no date that can be read,
rather than two thirds of the whole register.

---

## 3. The check of every other denominator

Run 2026-10-01, after the owner asked whether the same fault sat anywhere else.

**Method.** Every field's `Required:` clause was read from the publisher's own
dictionary, `data/raw/omb2025_data_dictionary.json`, and turned into a rule the
analysis applies to each row. The rule is in `src/conditionality.py`. A clause
the parser has not been taught raises and stops the build rather than defaulting
to "asked of every entry", because that default is what produced both faults
above.

**Three answers are possible for each entry and each field.** Asked, not asked,
and undetermined. 338 entries record no development stage, and every condition
written in terms of stage leaves those entries unplaceable. They are counted and
reported on their own. A figure that quietly puts them on one side states
something the file does not contain.

**Result.** 22 of the 31 fields the publisher's dictionary defines carry a
condition. Every one of them was being published as a share of all 3,611 rows.
Bold marks a conditional clause.

| Field | Required clause, verbatim | Share over all rows | Entries asked | Share where asked | Cannot be placed |
|---|---|---|---|---|---|
| `id` | Yes | 80.4% | 3,611 | 80.4% | 0 |
| `use_case_name` | Yes | 100.0% | 3,611 | 100.0% | 0 |
| `agency_bureau` | Yes | 98.4% | 3,611 | 98.4% | 0 |
| `is_withheld` | Yes | 68.7% | 3,611 | 68.7% | 0 |
| `development_stage` | Yes | 90.6% | 3,611 | 90.6% | 0 |
| `is_high_impact` | Yes | 88.2% | 3,611 | 88.2% | 0 |
| `HI_justification` | **Yes, but question should only appear if "Presumed high-impact, but determined not hig...** | 22.8% | 110 | 99.1% | 426 |
| `topic_area` | **Yes, for pre-deployment, pilot and deployed use cases.** | 83.3% | 2,959 | 99.3% | 338 |
| `classification` | **Yes, for pre-deployment, pilot and deployed use cases.** | 81.7% | 2,959 | 99.3% | 338 |
| `problem_solved` | **Yes, for pre-deployment, pilot and deployed use cases.** | 83.2% | 2,959 | 98.4% | 338 |
| `benefits` | **Yes, for pre-deployment, pilot and deployed use cases.** | 81.8% | 2,959 | 95.3% | 338 |
| `system_outputs` | **Yes, for pre-deployment, pilot and deployed use cases.** | 78.6% | 2,959 | 95.3% | 338 |
| `operational_date` | **Yes, for pilot and deployed use cases.** | 38.8% | 1,480 | 85.1% | 338 |
| `contracting_usage` | **Yes, for pilot and deployed use cases.** | 44.4% | 1,480 | 97.6% | 338 |
| `have_ato` | **Yes, for pilot and deployed use cases.** | 42.7% | 1,480 | 86.3% | 338 |
| `data_description` | **Yes, for pilot and deployed use cases.** | 34.3% | 1,480 | 76.6% | 338 |
| `link_to_data` | No | 3.0% | 3,611 | 3.0% | 0 |
| `has_pii` | **Yes, for pilot and deployed use cases.** | 41.8% | 1,480 | 85.9% | 338 |
| `pia_url` | No | 4.7% | 3,611 | 4.7% | 0 |
| `demographic_features` | **Yes, for pilot and deployed use cases.** | 30.6% | 1,480 | 65.5% | 338 |
| `has_custom_code` | **Yes, for pilot and deployed use cases.** | 47.4% | 1,480 | 97.0% | 338 |
| `code_url` | No | 4.7% | 3,611 | 4.7% | 0 |
| `hi_testing_conducted` | **Yes, only for high-impact deployed use cases** | 7.1% | 227 | 55.1% | 426 |
| `hi_assessment_completed` | **Yes, only for high-impact deployed use cases** | 6.5% | 227 | 55.5% | 426 |
| `hi_potential_impacts` | **Yes, only for high-impact deployed use cases** | 6.8% | 227 | 55.1% | 426 |
| `hi_independent_review` | **Yes, only for high-impact deployed use cases** | 7.4% | 227 | 55.1% | 426 |
| `hi_ongoing_monitoring` | **Yes, only for high-impact deployed use cases** | 7.4% | 227 | 55.1% | 426 |
| `hi_training_established` | **Yes, only for high-impact deployed use cases** | 7.8% | 227 | 55.1% | 426 |
| `hi_failsafe_presence` | **Yes, only for high-impact deployed use cases** | 8.1% | 227 | 55.5% | 426 |
| `hi_appeal_process` | **Yes, only for high-impact deployed use cases** | 8.0% | 227 | 55.5% | 426 |
| `hi_public_consultation` | **Yes, only for high-impact deployed use cases** | 7.3% | 227 | 55.5% | 426 |
Two columns in the derived file, `agency` and `agency_name`, are this project's
own and carry no clause. They are marked in the findings rather than left out.

**What was done.** `field_completeness_where_asked` was added to M2 and carries,
for every field, the verbatim clause, the number of entries the question is put
to, the share filled among those, and the number that cannot be placed. The
share over all rows is kept beside it. Both views are published, because for a
field asked of everything they agree, and where they disagree a reader should
see why.

**Field checked and found sound.** The withholding figure, 274 of the 445
entries marked high-impact with no status recorded. The dictionary states
`is_withheld` is *"Required: Yes"* with no condition, so the field is asked of
every entry in the register and 445 is a labelled subset rather than a wrong
denominator. The finding already published both that figure and the figure over
all 3,611 rows, and records `field_is_required` alongside them. No change.

**Fields checked and found sound.** `id`, `use_case_name`, `agency_bureau`,
`is_withheld`, `development_stage`, `is_high_impact`, and the three fields the
dictionary marks optional. All are asked of every entry, so the two shares
agree.

**Enforced by.** `tests/test_denominators.py`, five checks. Verified by planting
the failure each exists to catch.

---

## Standing rule this produced

A share published about a field is divided by the entries the publisher asks
that field of. Where that population is smaller than the register, both figures
are published and the narrower one is the one described as an unanswered
question. Where the population cannot be determined for some entries, those
entries are counted on their own and never folded into either side.
