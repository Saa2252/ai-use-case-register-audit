# Data provenance

Where every file came from, when it was downloaded, proof it has not changed
since, and what each field it uses actually means.

**Provenance** is the record that lets someone else check your work without
asking you for anything. **Hash** here means SHA-256, a fingerprint of a file's
contents. If one character changes, the fingerprint changes.

Status: Phase 3 run. Vendor, product and contact fields removed. T8 passes.
T2 does not yet pass, for one reason recorded in section 25.

**Reconciliation did not fully match. See section 3. The three gaps are present
in the source as published and are not artefacts of our download date. See
section 3.1.**

---

## 1. Sources

| Source | Official location | Licence | Use in this project |
|---|---|---|---|
| US OMB 2025 Federal Agency AI Use Case Inventory | https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory | US government work, public domain under 17 U.S.C. §105 | Core dataset |
| US OMB 2024 Federal AI Use Case Inventory | https://github.com/ombegov/2024-Federal-AI-Use-Case-Inventory | Same | **Schema reference only.** Field names, to establish which questions each year asks. No row-level use. See decision-rules.md section 11 |
| UK Algorithmic Transparency Recording Standard, template v4.0 | https://www.gov.uk/government/publications/algorithmic-transparency-template | Open Government Licence v3.0 | **Register design comparison.** The published template only: the field list organisations complete. No UK records are downloaded or read |
| Government of Ontario, AI use cases in the OPS | https://data.ontario.ca/dataset/artificial-intelligence-ai-use-cases-in-the-ontario-public-service | Open Government Licence - Ontario | **Reduced on 30 September 2026** to one observation: that it names no supplier in any published field. No longer the comparator. See decision-rules.md section 24 |

Both OMB repositories were on branch `main` at download. Neither carries a
notice of archival, relocation or supersession.

## 2. Downloaded files

All files downloaded by script (`src/provenance.py`), never by hand. Machine
manifest at `data/raw/manifest.json`, which is not committed.

| File | Source | Download date | SHA-256 | Bytes | Note |
|---|---|---|---|---|---|
| `omb2025_individually_reported.csv` | OMB 2025 | 2026-09-22 | `a62721202ca4b110ce3c53ffdb688d05ad27a35971a7afda4f1179b2493e31d0` | 3,132,295 | Core dataset |
| `omb2025_consolidated_cots.csv` | OMB 2025 | 2026-09-22 | `bd18984bdc41f8fc818c9d145de78ebe2563ee0ffab29fe7e96de4c223c8ba17` | 118,923 | Consolidated COTS, new in 2025 |
| `omb2025_data_dictionary.json` | OMB 2025 | 2026-09-22 | `4f968be4f1eae70159e6772239f34cacb3d8712881b425489fd68505c99a438d` | 45,220 | Data dictionary |
| `omb2025_data_dictionary.md` | OMB 2025 | 2026-09-22 | `bdc711b7eaf46bb844cf0cdf88fb984b5244c56a8f60cce410727ba22ff86476` | 26,116 | Data dictionary, readable form |
| `omb2025_README_datasets.md` | OMB 2025 | 2026-09-22 | `794c3d3042f7f2ca50ad61912bd39bde88dfeab74fd5eb3521f3bc7eb8750614` | 111 | Dataset notes |
| `omb2025_README.md` | OMB 2025 | 2026-09-22 | `c9cc8fc318466ba636c30f00e1f9a61e7088c782dbf8c3b573054070085a3cf9` | 10,688 | States the published totals |
| `omb2024_inventory_v1.csv` | OMB 2024 | 2026-09-22 | `9a2c9e25d41eb7b4b2e5463459c8ea78e0e02db0c15e82cc09c88e78889b40f5` | 2,655,883 | Version 1 |
| `omb2024_inventory_v2.csv` | OMB 2024 | 2026-09-22 | `789e1bac6d2551e8f90e5cfc5feb37ac23c6ca9f302f5af92fea8a577caa0a83` | 2,982,726 | Version 2. **This is the version used.** Its row count of 2,133 matches the total the 2024 README states; version 1 does not. Recorded 30 September 2026, closing a note that had stood open since Phase 1. The choice affects field names only, since no row of either file is read |
| `omb2024_data_dictionary.yaml` | OMB 2024 | 2026-09-22 | `bc2302170a5b3aee419479522cd6afbb5416de9555a8d6fe7e34a848d7e8eee0` | 45,842 | Data dictionary |
| `omb2024_README.md` | OMB 2024 | 2026-09-22 | `dc846005495e339b6a77a38030a973d1dfec53648611de72ea045edc5275ea7f` | 6,096 | States the 2024 totals |
| `uk_atrs_template_v4.xlsx` | UK ATRS | 2026-09-30 | `11e9f903e9c82525c1fc92ad66a59ae7e98d378f12c13311b8193a7fd0cb2eab` | 276,411 | The published field template, v4.0. Read for its field list and its lists of allowed answers. Downloaded by `src/provenance.py` like every other file |
| `ontario_ai_use_cases_en.csv` | Ontario | 2026-09-22 | `f5bbd7d0c2b14d3f1a2f5ea9a982e7ef28d5b59a83a1f483104d9c98089ade7a` | 2,182 | English, the version analysed |
| `ontario_ai_use_cases_fr.csv` | Ontario | 2026-09-22 | `6d0a01e8bc5df75c89d35a935719e7b9004adb24dd8510239ef7733bf9700a7a` | 3,037 | French translation, NOT analysed, recorded so the register is not read as twice its size |

### Encoding

`omb2024_inventory_v2.csv` is **not UTF-8**. It decodes as cp1252. Reading it as
UTF-8 raises an error at byte 271. Any re-run must declare the encoding
explicitly, or the file will appear unreadable rather than different.

### Archived copies (S1)

The 2025 repository states that updates are processed on a rolling basis, and
one agency's inventory is listed as forthcoming, so the pages will change.

| Page | Archived copy | Captured |
|---|---|---|
| 2025 repository | http://web.archive.org/web/20260922175845/https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory | 2026-09-22, on request from this project |
| 2024 repository | http://web.archive.org/web/20260824051210/https://github.com/ombegov/2024-Federal-AI-Use-Case-Inventory | 2026-08-24, pre-existing capture |

**Honest limit.** The archive service refused a new capture of the 2024 page,
returning a server error on two attempts. The link above is a pre-existing
capture from 24 August 2026, about a month before this project downloaded the
data. It is not a capture of the page as read on 22 September 2026. A retry is
worth making later.

## 3. Reconciliation to published totals (S6)

Every figure stated in the 2025 README, checked against the downloaded files.

| Figure stated by the source | Stated | Observed | Result |
|---|---|---|---|
| Individually reported AI use cases | 3,611 | 3,611 rows | Match |
| High-impact AI use cases | 445 | 445 rows where `is_high_impact` is "High-impact" | Match |
| Deployed and piloted AI use cases | 1,818 | 1,480 rows where `development_stage` is "Deployed" or "Pilot" | **Does not match** |
| Total agency submissions | 56 | 54 agency rows in the source's own table | **Does not match** |
| Agency submissions, individually reported | 41 | 41 distinct agencies in the file | Match |
| Agency submissions, consolidated COTS | 46 | 45 distinct agencies in the file, and 45 rows marked Y in the source's own table | **Does not match** |
| Agencies affirmatively reporting no AI | 2 | 2 rows so marked in the source's own table | Match |

### Where the deployed-and-piloted gap sits

| `development_stage` | Rows |
|---|---|
| Pre-deployment | 1,479 |
| Deployed | 1,040 |
| Pilot | 440 |
| Retired | 314 |
| blank | 338 |

Deployed plus Pilot is 1,480. The stated figure is 1,818. The difference is 338,
which is exactly the number of rows with a blank `development_stage`.

That arithmetic is an observation, not an explanation. It is consistent with the
published figure counting blank-stage rows, and equally consistent with the
stage field having been cleared for those rows after the figure was produced.
The data cannot separate the two.

### Internal disagreement inside the source's own table

Summing the per-agency rows of the README table and comparing with the table's
own TOTALS row. 41 rows carry numbers. 13 carry text instead.

| Column | Rows with numbers | Rows with text | Sum of the rows | TOTALS row states | Difference |
|---|---|---|---|---|---|
| Total Publicly Reported AI Use Cases | 41 | 13 | 3,611 | 3,611 | 0 |
| Deployed and Piloted AI Use Cases | 41 | 13 | 1,819 | 1,818 | **+1** |
| High-Impact Use Cases | 41 | 13 | 445 | 445 | 0 |

The deployed and piloted column does not add up to its own stated total. The
discrepancy is one.

The four text values appearing in place of numbers:

- "This agency has no individual AI use cases to report"
- "This office has no individual AI use cases to report"
- "Reported to OMB their agency does not use AI"
- "This agency's public AI inventory is forthcoming"

These are distinct states and are not the same as zero. One agency's inventory
is still forthcoming, so the published figures are not final.

## 4. Field inventory by year (S1, and the owner's amendment of 22 September 2026)

The source states that the number of reporting questions was reduced between the
two years. Confirmed by counting fields.

| File | Rows | Fields |
|---|---|---|
| 2025 individually reported | 3,611 | 36 |
| 2025 consolidated COTS | 900 | 5 |
| 2024 inventory (v2) | 2,133 | 62 |
| Ontario, English | 3 | 9 |

Full field lists captured at `data/raw/field_inventory.json`.

**Field completeness is therefore not comparable across years.** A field that is
blank in 2025 may not exist in 2025 at all. Completeness is reported within a
year only. This is now on the stop-and-ask list.

### Which 2024 file is authoritative

The 2024 repository publishes two versions of the same inventory.

| File | Rows | Verdict |
|---|---|---|
| `2024_consolidated_ai_inventory_raw.csv` | 1,757 | Not used |
| `2024_consolidated_ai_inventory_raw_v2.csv` | 2,133 | **Used.** Row count matches the 2,133 the 2024 README states |

Note on wording: "consolidated" in the 2024 file name means consolidated across
agencies, that is, the combined inventory. It does **not** mean the 2025 sense
of consolidated commercial off-the-shelf reporting. Same word, different
meaning, and a real trap when reading the two years together.

## 5. Cross-year identifier comparability

**Conclusion: identifiers are not comparable across years. They do not exist in
2024.**

| Year | Identifier field | Evidence |
|---|---|---|
| 2025 | `id` | Present in the 2025 individually reported file |
| 2024 | none | No identifier column of any kind among the 62 fields. Columns are full question text, not coded fields |

This is a stop-and-ask condition under the brief. The entry-level crosswalk
authorised by the owner cannot run on identifiers. Any alternative, such as
matching on use case name and agency, is a weaker method with its own error
rate, and is the owner's decision, not this project's.

## 6. Department of War exclusion (owner's amendment of 22 September 2026)

Department of War use cases are excluded from the 2025 inventory. The question
was whether that agency reported in 2024, because its entries would then need
separating out of the carry-forward analysis.

**It did not.** No agency matching War, Defense or Defence appears among the 42
agency strings in the 2024 file. The Department of Defense is absent from the
2024 public inventory.

The 2025 exclusion therefore has no carry-forward consequence. No entries need
separating out. The exclusion remains worth stating in the README as a scope
limit of the underlying data.

Note on agency name quality: the 2024 file contains "Department of Veterans
Affairs" twice, the two differing only by trailing whitespace. Agency names
require normalisation before any matching in Phase 2.

## 7. Category definition by year

The serious category is defined differently in each year. See
`governance/decision-rules.md` section 4 for the owner's ruling on how this may
and may not be reported.

| Year | Governing memorandum | Field in file | Values observed |
|---|---|---|---|
| 2024 | OMB M-24-10 | `Is the AI use case rights-impacting, safety-impacting, both, or neither?` | to be tabulated in Phase 2 |
| 2025 | OMB M-25-21 | `is_high_impact` | High-impact (445), Not High-impact (2,630), Presumed High-Impact but Not High-impact (110), blank (426) |

Dictionary definitions for both years belong to Phase 2 and are not yet
recorded.

### Presumed high-impact but determined not high-impact

Requested by the owner as input to the Phase 4 decision on the M4 subset.

| Item | Value |
|---|---|
| Entries carrying the status | **110** |
| The data's own label, verbatim | `Presumed High-Impact, but Not High-impact` |
| Justification field exists | Yes, `HI_justification` |
| Justification field completeness for those 110 | to be measured in Phase 2 |

Also observed: `is_high_impact` is blank for 426 rows. A three-state field with
a substantial blank category is really four states. This needs addressing before
M4 can define its subset.

## 8. Consolidated off-the-shelf reporting (2025 only)

| Item | Value |
|---|---|
| File | `2025_consolidated_COTS_AI_use_cases.csv` |
| Rows | 900 |
| Fields | Agency, AI Use Case, Agency Use (Y/N)?, Name of Commercial Product or Service Used, Estimated # of Licenses/Users |
| Distinct agencies | 45 |
| Rows marked Y | 468 |
| Rows marked N | 416 |
| Rows blank | 16 |

The file is a grid of agency against common task, not a list of individual use
cases. It carries a task name and a product name but **no use case identifier**,
so a 2024 entry cannot be matched into it at entry level. The check the owner
specified is possible at agency and task level only.

Correction recorded: an earlier note in this project claimed that a 2024
rights-impacting or safety-impacting flag made a case ineligible for 2025
consolidated reporting. That was wrong. Eligibility is judged against the 2025
high-impact definition, assessed in 2025, and a case flagged in 2024 could be
determined not high-impact in 2025 and become eligible. The correct label is
"unlikely to be explained by consolidated reporting", not "cannot".

## 9. Fields to remove before publication

Identified at download. Removal happens in Phase 3.

| Field | File | Reason | Safeguard |
|---|---|---|---|
| `contact_email` | 2025 individually reported | Personal data | S8 |
| `vendor_name` | 2025 individually reported | Vendor name | S2 |
| `Name of Commercial Product or Service Used` | 2025 consolidated COTS | Product name | S2 |
| `Is the AI use case found in the below list of general commercial AI products and services?` | 2024 inventory | Product reference | S2 |
| `system_name_ato` | 2025 individually reported | May carry product names, to check | S2 |

## 10. Ontario

| Item | Value |
|---|---|
| Title | Artificial Intelligence (AI) use cases in the Ontario Public Service |
| Licence | Open Government Licence - Ontario, OGL-ON-1.0 |
| Licence page | https://www.ontario.ca/page/open-government-licence-ontario |
| Last updated at source | 2026-06-09 |
| Files published | Two CSVs, English and a French translation |
| **Rows in the English file** | **3** |
| Fields | 9 |

The English file is the one analysed. The French file is recorded so that nobody
later reads the register as twice its actual size.

**The Ontario register contains three entries.** The brief anticipated that
Ontario is small and directed that the comparison be about design rather than
volume. Three rows is smaller than that framing assumes, and the owner should
decide whether M5 still holds as written.

Ontario fields: AI use case name, Ministry, Use Case Description, Launch Date,
AI Capabilities, Autonomous, Human in the loop, User base, What data is used?

Note that Ontario asks about autonomy and human-in-the-loop as standing fields,
and names no vendor. That is the design point M5 was built to make, and it
survives regardless of row count.

### Ontario licence attribution

Required by the licence and by S1. Copied verbatim from the licence page at
https://www.ontario.ca/page/open-government-licence-ontario on 23 September 2026.

The licence requires the attribution statement specified by the Information
Provider. The dataset's published metadata specifies none, and the licence text
states that where no specific statement is given, the following must be used:

> Contains information licensed under the Open Government Licence – Ontario.

### UK licence attribution

Required by the licence and by S1. The Open Government Licence v3.0 sets this
wording for use where the Information Provider publishes no attribution
statement of its own. Copied verbatim from the licence at
https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/ on
1 October 2026.

> Contains public sector information licensed under the Open Government Licence v3.0.

The publication also carries "© Crown copyright". Both appear on every page
where material derived from the UK template is shown, which is `gaps.html` and
`index.html`, and in the disclaimer on every page. Held once in
`src/disclaimer.py` as `UK_ATTRIBUTION` and rendered by `scripts/build_site.py`.

This statement appears on every page where Ontario-derived data is shown, with a
link to the licence.

## 3.1 Publication timeline, and why drift is ruled out

The owner asked whether the three gaps could be explained by the data changing
after the summary was written, since the summary is dated 13 April 2026 and this
project downloaded on 22 September 2026, with updates processed on a rolling
basis.

Commit history of the 2025 repository answers it.

| Item | Last changed | What changed |
|---|---|---|
| `Data/2025_individually_reported_AI_use_cases.csv` | 2026-04-14 14:33 UTC | Uploaded once. Never changed since |
| `Data/2025_consolidated_COTS_AI_use_cases.csv` | 2026-04-14 14:33 UTC | Uploaded once. Never changed since |
| `README.md` | 2026-05-14 12:36 UTC | One row of the per-agency table restated in words. No figure altered |
| `README.md` | 2026-04-14 15:03 UTC | The summary figures and the per-agency table were added, about 30 minutes after the data files were uploaded |

**Drift is ruled out as an explanation.** The data files have not changed since
14 April 2026. The summary figures were written against those files on the same
day. The only later edit replaced the text in one agency's row and touched no
number.

The three candidate explanations for each gap are therefore reduced from three
to two, and the remaining two are recorded with each finding in section 3.

## 11. The 2024 file versions

The 2024 repository publishes two files with near-identical names. They are not
documented as a pair.

| File | Rows | Encoding | Named in the 2024 README repository structure |
|---|---|---|---|
| `2024_consolidated_ai_inventory_raw.csv` | 1,757 | UTF-8 | **Yes** |
| `2024_consolidated_ai_inventory_raw_v2.csv` | 2,133 | cp1252 | **No** |

The 2024 README states 2,133 use cases and 41 agency submissions, as of
23 January 2025.

So the two files point in opposite directions:

- The README's repository structure names **v1** and does not mention v2.
- The README's stated total of 2,133 matches **v2** exactly, and 1,757 matches
  v1 exactly.
- After normalising for whitespace, v2 contains 41 distinct agency names, which
  also matches the stated 41 agency submissions.

**This project uses v2**, because two independently stated figures match it and
neither matches v1. The choice is recorded rather than assumed, and the fact
that the README names the other file is published alongside it.

## 12. Cross-year identifiers: the finding and its cause

The entry-level crosswalk is dropped. The cause is published as the finding.

### 2024

No identifier field of any kind among the 62 columns. Columns are full question
text. Entries cannot be tracked between years.

### 2025

An `id` field exists. Its dictionary entry says a unique identifier for the AI
use case, that use cases should maintain the same ID if included in the previous
year's inventory, and that agencies are permitted to remove the Use Case ID
column from their own public inventories.

**Correction to an earlier characterisation in this project:** the instruction is
that identifiers should be *carried over unchanged* between years, not that they
should not be repeated. Repetition across years is the mechanism that makes
tracking work. The conclusion is unaffected: tracking becomes possible from 2025
onward. The reason is identifier stability.

### The 2025 id field as published

| Item | Value |
|---|---|
| Rows | 3,611 |
| Rows with an id | 2,907 (80.5%) |
| Rows with no id | 704 (19.5%) |
| Distinct id values | 2,892 |
| Id values appearing on more than one row | 13, affecting 28 rows |

**The field is neither complete nor unique as published.** Tracking from 2025
onward is possible in principle and is not yet reliable in practice. Both halves
belong in the finding.

## 13. Classification bands in 2025 (M4 subset rule)

The owner's rule, decided 22 September 2026, is recorded in
`governance/decision-rules.md` section 9.

| Band | Rows |
|---|---|
| High-impact | 445 |
| Not High-impact | 2,630 |
| Presumed High-Impact, but Not High-impact | 110 |
| Classification not recorded (blank) | 426 |
| **Total** | **3,611** |

445 + 2,630 + 110 + 426 = 3,611. The arithmetic closes against the file.

### The justification field

`HI_justification` dictionary instruction: provide a justification for why the
use case is determined to be not high-impact, and the question should only
appear if "Presumed high-impact, but determined not high-impact" is selected.

| Band | Rows | Justification filled | Fill rate |
|---|---|---|---|
| Presumed High-Impact, but Not High-impact | 110 | 109 | 99.1% |
| High-impact | 445 | 6 | 1.3% |
| Not High-impact | 2,630 | 712 | 27.1% |
| Classification not recorded | 426 | 0 | 0.0% |

The band the field was designed for is filled in 109 of 110 rows. The field is
also populated in 718 rows outside that band, where the dictionary says the
question should not have appeared. Recorded as an observation about the
structure of the data. No inference is drawn about any agency.

## 14. Methods note: reliability of name-plus-agency matching

Run solely to quantify the unreliability of the method that was rejected. **No
conclusion is drawn from it about missing or carried-forward entries.**

Method: agency name and use case name, lowercased, punctuation stripped,
whitespace collapsed, joined into one key.

| Measure | 2024 | 2025 |
|---|---|---|
| Rows | 2,133 | 3,611 |
| Distinct agency-plus-name keys | 2,049 | 3,542 |
| Rows sharing a key with another row in the same year | 116 (5.4%) | 97 (2.7%) |
| Rows sharing a use case name with another row, ignoring agency | 133 (6.2%) | 135 (3.7%) |
| Distinct agency names after normalisation | 41 | 41 |

Agencies whose normalised name appears in both years: 31 of 41.

**Why the method is not fit for carry-forward conclusions:**

1. The key is not unique inside a single year. 116 rows in 2024 and 97 in 2025
   share a key with at least one other row, so matching cannot be one-to-one for
   those rows in either direction.
2. Ten of 41 agency names do not correspond across years after normalisation, so
   a non-match may be a naming difference rather than an absent entry.
3. Of the keys that do appear in both years, 13 are ambiguous, matching more
   than one row on at least one side.
4. A use case may be renamed between years while remaining the same system, and
   two different systems may carry the same name. The method cannot tell either
   case apart.

**One figure produced by this run is permanently out of scope.** The overlap
count between years reads as a carry-forward rate whatever caveat is attached to
it. On 23 September 2026 the owner reclassified the 2024 inventory as a schema
reference with no row-level use, which forbids the analysis that produced this
figure. It is not withheld pending review. There is no later phase in which it
becomes publishable.

This methods note is retained because it records why a method was rejected. The
measures in the table above describe the properties of the matching key, not any
entry.

---

# Phase 2: profile

## 15. Fields present in the file but absent from the dictionary

The 2025 dictionary documents **34** fields. The published file has **36**
columns.

| Column in file | In dictionary |
|---|---|
| `agency` | **No** |
| `agency_name` | **No** |

Every other column is documented, and no documented field is missing from the
file.

Both undocumented columns are used by this project, `agency_name` for row-level
detail and `agency` as its short form. Under the brief this is a stop-and-ask
condition, because a field being used has no dictionary definition. The values
are self-evident and consistent, so the practical risk is low, but the gap is
recorded rather than assumed away.

## 16. Conditional fields and their fill patterns

Three fields carry conditional instructions. All three use the same wording
pattern: "Required: Yes, but question should only appear if X is selected for
the previous question."

### Is the wording unambiguous?

Largely, with one important qualification. The instruction describes **the
behaviour of the collection form**, that is, when the question is shown. It is
not written as a validation rule on the resulting data, and it says "should"
rather than "must". It also refers to "the previous question", which depends on
the ordering of the original Excel instrument rather than on the published
column order.

So a value appearing outside the stated condition does not contradict an
explicit prohibition. It indicates that the value reached the file by a path the
instruction does not describe.

### Fill patterns against the stated condition

| Field | Condition | Rows meeting it | Filled | Rows not meeting it | Filled |
|---|---|---|---|---|---|
| `HI_justification` | classification is presumed-but-determined-not | 110 | 109 (99.1%) | 3,501 | **718 (20.5%)** |
| `vendor_name` | purchased from a vendor, or both, and stage is pilot or deployed | 552 | 392 (71.0%) | 3,059 | **398 (13.0%)** |
| `system_name_ato` | has an ATO, and stage is pilot or deployed | 681 | 623 (91.5%) | 2,930 | **283 (9.7%)** |

**The pattern is not confined to one field.** All three conditional fields carry
values in rows that do not meet the stated condition. This is a property of the
data as published, described against the dictionary as published.

### Clustering of the 718

Reported as an observation. No explanation is offered.

- 9 of 41 agencies account for all 718 rows. The other 32 have none.
- The three largest hold 599 of 718, which is 83.4%.
- Four agencies show the pattern in 100% of their rows.

The pattern is concentrated by submission rather than spread across the file.

## 17. Completeness profile, and a trap inside it

### The trap

Two fields store an empty answer as the literal two-character string `[]`, which
is neither null nor an empty string.

| Field | Rows holding `[]` |
|---|---|
| `demographic_features` | 2,507 |
| `hi_public_consultation` | 3,346 |

A naive completeness test counts `[]` as filled and reports both fields at
100%. Corrected, `demographic_features` is 30.6% and `hi_public_consultation`
is 7.3%.

Recorded because it would have produced two published figures that were wrong by
roughly seventy percentage points, in the direction that flatters the register.
All completeness figures in this project treat `[]` as empty.

### Selected completeness, corrected

Percentage of rows where the field holds a real value. Full table at
`data/raw/completeness_2025.json`.

| Field | All 3,611 rows | The 445 high-impact rows |
|---|---|---|
| `use_case_name` | 100.0% | 100.0% |
| `id` | 80.5% | 96.9% |
| `development_stage` | 90.6% | 100.0% |
| `is_high_impact` | 88.2% | 100.0% |
| `operational_date` | 38.8% | 33.3% |
| `has_pii` | 41.8% | 34.4% |
| `demographic_features` | 30.6% | 22.0% |
| `hi_testing_conducted` | 7.1% | 28.5% |
| `hi_assessment_completed` | 6.5% | 28.8% |
| `hi_independent_review` | 7.4% | 28.5% |
| `hi_ongoing_monitoring` | 7.4% | 28.5% |
| `hi_failsafe_presence` | 8.1% | 28.8% |
| `hi_appeal_process` | 8.0% | 28.8% |

### The oversight block behaves as one unit

Within the 445 high-impact rows, the nine oversight fields all sit between 28.5%
and 28.8%. That is not nine independent rates. Counting how many of the nine
each row answers:

| Oversight fields answered | Rows |
|---|---|
| All nine | 126 |
| None | 317 |
| Between one and eight | 2 |

The block is present or absent as a whole. Two rows out of 445 are partial.

Clustering, again an observation only: of the agencies with the most high-impact
entries, one holds 215 such rows with none answering the block, while two others
hold 114 and 55 with 73 and 39 answering it in full.

**Mandatory caveat wherever this appears:** a filled field shows that
information was provided. It does not show that the practice described is
adequate. An empty field is not evidence that the practice is absent.

## 18. Personal data identified for removal (S8)

| Field | Finding | Action in Phase 3 |
|---|---|---|
| `contact_email` | Email addresses in 2,328 rows | Column dropped entirely |
| `problem_solved` | One email address inside free text | Scrubbed from free text |

No phone-number patterns were found in any field.

## 19. Vendor and product fields identified for removal (S2)

| Field | Source | Action |
|---|---|---|
| `vendor_name` | 2025 individually reported | Column dropped. Populated in 790 rows |
| `system_name_ato` | 2025 individually reported | Column dropped. May carry product names |
| `Name of Commercial Product or Service Used` | 2025 consolidated COTS | Column dropped |
| `Is the AI use case found in the below list of general commercial AI products and services?` | 2024 inventory | Column dropped |

Free-text fields are scanned separately in Phase 3 and vendor mentions replaced
with `[product]`.

## 20. Cross-year field sets

Confirming the source's statement that the number of reporting questions was
reduced. 2024 asked 62. 2025 asks 36.

### In 2025, with no equivalent in 2024

| Field | What it captures |
|---|---|
| `id` | Unique use case identifier. The basis of any year-to-year tracking |
| `contact_email` | A named contact for the entry |
| `is_withheld` | Whether the entry is withheld from public reporting, and on what ground |
| `HI_justification` | Why a presumed high-impact case was determined not to be |
| `classification` | The AI classification of the system |
| `link_to_data` | Link to the underlying data where it must be disclosed |
| `pia_url` | Link to the privacy impact assessment |
| `vendor_name` | Named vendor. 2024 asked for a procurement identifier instead |
| `hi_training_established` | Whether operator training is established |

### In 2024, with no equivalent in 2025

Grouped, because the list is long.

| Group | 2024 fields | Note |
|---|---|---|
| **Autonomy** | Can the AI carry out a decision or action without direct human involvement | **No 2025 equivalent.** See below |
| **Adverse influence** | Whether the AI significantly influences decisions with possible adverse effect | No 2025 equivalent |
| Dates | Date Initiated, Date Acquisition or Development began, Date Implemented, Date Retired | Four date fields. 2025 asks one, `operational_date` |
| Public service delivery | Supporting a High-Impact Service Provider, which one, which service | Three fields, none carried forward |
| Public notice | How notice is given when people interact with the AI | Not carried forward |
| Disparities | Steps taken to detect and mitigate performance disparities across demographic groups | Not carried forward as a question. 2025 asks only which demographic variables are used |
| Privacy governance | Whether the Senior Agency Official for Privacy assessed the risks | 2025 asks for a link to the assessment instead |
| Information quality | Compliance with Information Quality Act guidance, dissemination to the public | Not carried forward |
| Procurement | Procurement Instrument Identifier | 2025 asks for the vendor name instead |
| Capacity and tooling | Waiting time for developer tools, compute access process, infrastructure intake, internal review and feedback, extension requests | Six fields, none carried forward |
| Free-text overflow | Eight "If Other, please explain" fields | Structural, not substantive |

### The autonomy question

2024 asked whether the AI can carry out a decision or action without direct
human involvement. **2025 does not ask it.**

This matters to M5. Ontario asks about autonomy and about human-in-the-loop as
standing fields in a nine-field register. The 2025 federal register, at 36
fields, asks neither. That is a comparison of what each register asks, which is
what M5 is for, and it does not depend on the size of either register.

## 21. Field mapping to dictionary definitions

Every 2025 field used by this project, mapped to its dictionary entry. The
dictionary is at `data/raw/omb2025_data_dictionary.json`, hash recorded in
section 2.

| Field | Original Excel header | Used for |
|---|---|---|
| `id` | Use Case ID | Identifier finding, cross-year tracking |
| `use_case_name` | Use Case Name | M1 near-duplicate detection, row-level detail |
| `agency_name` | not in dictionary | Row-level detail, clustering observations |
| `development_stage` | Stage of Development | M3 freshness, reconciliation |
| `is_high_impact` | Is the AI use case high-impact? | M4 subset, band arithmetic |
| `HI_justification` | Justification | M4 band reporting, conditional-field finding |
| `operational_date` | Date when AI use case became operational or the pilot's start date | M3 freshness |
| `contracting_usage` | Was the system purchased from a vendor or developed in-house | Conditional-field finding |
| `have_ato` | Does this use case have an associated ATO? | Conditional-field finding |
| `topic_area` | Use Case Topic Area | M1 profiling |
| `has_pii` | Does this use case involve PII? | M2 completeness |
| `demographic_features` | Which demographic variables does the use case explicitly use | M2 completeness |
| `hi_testing_conducted` | Has pre-deployment testing been conducted? | M4 oversight block |
| `hi_assessment_completed` | Has an AI impact assessment been completed? | M4 oversight block |
| `hi_potential_impacts` | What are the potential impacts of using the AI | M4 oversight block |
| `hi_independent_review` | Has an independent review been conducted? | M4 oversight block |
| `hi_ongoing_monitoring` | Is there a process for ongoing monitoring | M4 oversight block |
| `hi_training_established` | Has the agency established training for operators | M4 oversight block |
| `hi_failsafe_presence` | Does this use case have an appropriate fail-safe | M4 oversight block |
| `hi_appeal_process` | Is there an established appeal process | M4 oversight block |
| `hi_public_consultation` | What steps has the agency taken to consult affected groups | M4 oversight block |

## 22. Scope limit on the 2024 inventory

**Binding from 23 September 2026.** Full ruling in `governance/decision-rules.md`
section 11.

The 2024 inventory is a **schema reference**. Its only permitted use is
establishing which questions each year asks, recorded in section 20.

| Use | Permitted |
|---|---|
| Listing its field names | Yes |
| Reading its rows for any other purpose | **No** |
| Comparing any count with a 2025 count | **No** |
| Matching entries between years | **No** |
| Completeness figures, for 2024 or compared across years | **No** |
| Category comparison between years | **No** |
| Any headline built on it | **No** |

Two findings survive, because both concern the repository rather than its rows:
the cp1252 encoding (section 11 above) and the two near-identically named files
whose documentation and row counts point at different files (section 11 above).
Both are published as findings about reusability.

The row counts recorded elsewhere in this document (1,757 and 2,133) are
retained as evidence for the two-file finding. They are not available for
comparison with any 2025 figure.

---

# Phase 3: scrub

Counts only. No vendor or product term appears in this document or in any
committed file. The term list lives in `data/raw/vendor_terms.txt`, which is
gitignored.

## 23. What was removed

| Action | Count |
|---|---|
| Columns dropped entirely | 4 |
| Vendor or product mentions replaced with `[product]` | **1,339** |
| Rows affected by at least one replacement | 663 |
| Email addresses removed from free text | 1 |
| Phone numbers found anywhere | 0 |
| Terms on the final vendor list | 892 |

### Columns dropped

| Column | File | Reason |
|---|---|---|
| `vendor_name` | 2025 individually reported | Names a vendor (S2) |
| `system_name_ato` | 2025 individually reported | May name a product (S2) |
| `contact_email` | 2025 individually reported | Personal data, addresses in 2,328 rows (S8) |
| Product or service name column | 2025 consolidated COTS | Names a product (S2) |

### Outputs

| File | Rows | Columns |
|---|---|---|
| `data/derived/register_2025_scrubbed.csv` | 3,611 | 33 |
| `data/derived/cots_2025_scrubbed.csv` | 900 | 4 |

Row counts are unchanged from the raw files. Nothing was dropped at row level.

## 24. How the term list was built

Assembled from the vendor and product columns of the **2025** files only, plus a
manual list of common commercial AI vendors and products. The 2024 inventory is
a schema reference and its rows are not read.

Under the owner's rule of 23 September 2026, S2 targets **commercial companies
and their commercial products**. A term qualifies only if it is a proper noun,
is not a controlled-vocabulary value, and is not a multi-word generic phrase.

### Replacement count at each stage

| Stage | Replacements | What changed |
|---|---|---|
| Unfiltered term list | 4,662 | Every distinct value from the vendor columns |
| Ordinary vocabulary, agency names and controlled values removed | 1,637 | Words such as those for decisions and searching were never vendor names |
| Commercial-only rule applied | 1,540 | Proper-noun, generic-phrase and open-source filters |
| **Final** | **1,339** | Ordinary-word brand names handled separately, real mentions restored on evidence |

The reduction from 4,662 is not a loosened safeguard. It is the removal of
matches that were never vendor names.

### Open-source terms retained

Published at `data/derived/open_source_terms_retained.json`. These describe the
technology used rather than identifying a commercial supplier, so they are not
removed.

### Ordinary-word brand names held back

Six terms are company or product names that are also ordinary English words:
those meaning a location, a container, a pleasant quality, a guard, a finding
tool and a day of work. Each was checked in context in the scrubbed output. None
appears as a commercial reference in this register. They are held off the list
because a case-insensitive rule on them would scrub ordinary prose.

Three others were checked the same way, found to carry **real** commercial
mentions, and restored: two matched case-sensitively, and one company domain
found inside a link.

## 25. Test status after Phase 3

| Test | Enforces | Status |
|---|---|---|
| T8 no personal data | S8 | **Passes** |
| T2 no vendor terms | S2 | **One failure remains.** See below |

### The remaining T2 failure

One word, once, in the derived register: an adjective in the phrase "spheroidal
elastic deformation sources", describing a physical property in a geophysics use
case. A company shares the word.

This is the same structural problem as the six held-back terms, arriving from
the other direction. The company has one real mention in the register, which is
removed by matching the capitalised form. The lowercase adjective in ordinary
prose is what T2 matches, because T2 is case-insensitive by design.

The options are all safeguard decisions and none has been taken:

1. Hold the term back like the other six, which leaves the one real mention.
2. Add a third exact-string exemption, which the owner has made a stop-and-ask.
3. Allow T2 to match case-sensitively for a documented subset of terms.

### An incident recorded in full

An earlier run of this phase removed two real company names from the term list
because they collided with markup and a stylesheet keyword. T2 then passed.
Checking the output showed both companies still named in the register, including
one in a link to a company research page. Removing a term from the list the test
reads is weakening the test to make it pass, which the brief forbids. Both terms
were restored, the data was re-scrubbed, and the collision was escalated.

## 26. The empty-list finding (reusability)

Two fields record "nothing selected" as the literal two-character text `[]`,
which is neither null nor an empty string. **Standard tools read those two
characters as content.**

| Field | Read naively | Corrected |
|---|---|---|
| `demographic_features` | **100.0%** | **30.6%** |
| `hi_public_consultation` | **100.0%** | **7.3%** |

A register published for reuse is only reusable if a reader counting it arrives
at the right number. Anyone profiling these two fields without inspecting the
values first would publish a completeness figure roughly seventy percentage
points too high, in the direction that flatters the register.

This finding is in the same class as the encoding finding in section 11: both
concern whether published data can be picked up and used correctly.

## 27. Placeholder scan and the empty-value rule

Every text field was scanned for values recording an absence rather than an
answer. The rule is at `data/raw/empty_value_rule.json` and every completeness
figure in the project is computed under it.

### What the scan found

| Pattern | Where |
|---|---|
| `[]` | 3,346 and 2,507 rows in two fields |
| "Not available", "Not Available" | Across seven fields |
| "TBD", "To be determined" | Across six fields, including the identifier field |
| "unknown", "Unknown" | Across four fields |
| "No" in a URL or description field | 66, 65, 40 and 6 rows in four fields |
| "N/a", "na", "none" | Small counts across three fields |

No whitespace-only values and no single-space values were found.

### The distinction the scan forced

A value is an absence only in a field expecting written content or a URL. In a
multiple-choice field the same string can be a valid selection. The dictionary
lists "b) Not applicable" as an allowed answer to the appeal-process and
fail-safe questions, so there it is counted as an answer.

Applying it as a blanket rule would have moved those two oversight fields from
28.8% to 26.5% and 22.0% and broken the oversight-block finding, on a mistake.

### Figures that moved after the rescan

| Figure | Before | After |
|---|---|---|
| Rows with no usable identifier | 704 | **706** |
| `link_to_data` filled | 5.7% | 3.0% |
| `code_url` filled | 6.9% | 4.7% |
| `pia_url` filled | 6.5% | 4.7% |
| `data_description` filled | 35.7% | 34.3% |
| `HI_justification` filled, high-impact band | 1.3% | **1.1%** |

The oversight block is unchanged at 126 all, 317 none, 2 partial.

**The identifier headline changes to 706.** The two extra rows carry "TBD" in
the identifier field.

**The rule on the justification figure now attaches to 1.1%.** It never appears
without the dictionary explanation in the same paragraph.

## 28. Undocumented columns: documented gap and finding

**Finding:** the published file carries 36 columns. The dictionary documents 34.

The two undocumented columns are the agency code and the agency name. Both are
used by this project.

Verified before relying on them:

| Check | Result |
|---|---|
| Distinct agency codes | 41 |
| Distinct agency names | 41 |
| Codes mapping to more than one name | 0 |
| Names mapping to more than one code | 0 |
| Names differing only by whitespace or case | 0 |

The mapping is one-to-one in both directions. No clustering count reported
earlier needs restating.

## 29. Date fields and whether M3 can be built

Reported before Phase 4 opens, because the freshness rule and the View 1 toggle
depend on the answer.

### What date fields exist

**One.** `operational_date`, typed as a date in the dictionary, defined as the
date the use case became fully operational or the pilot's start date, and
required for pilot and deployed use cases only.

The 2024 inventory asked four date questions. The 2025 field set contains one.

### Its condition

| Measure | Value |
|---|---|
| Rows carrying a value | 1,402 of 3,611 (38.8%) |
| Of those, values that parse as a date | 1,144 (81.6%) |
| **Usable dates as a share of all rows** | **31.7%** |
| Range of parsed values | 1990 to 2027 |
| Values dated after today | 5 |

Fill tracks the dictionary's condition, as expected: 82.7% for deployed entries
and 90.7% for pilots, against 9.3% for pre-deployment and 1.6% for retired
entries.

**For the high-impact subset the rate is 33.3%.**

The 258 values that do not parse take a form such as a three-letter month
followed by a two-digit number. These cannot be resolved to a year or a day
without guessing, and guessing would manufacture precision the file does not
contain. Recorded as reusability finding R4.

### Is there a field recording when an entry was last checked?

**No.** No field in the 2025 set records a review date, a verification date, an
update date or a last-modified date. The only field whose name suggests review
asks whether an independent review has taken place, and its answer is a
selection, not a date.

The two data files were uploaded once and have not changed since, so every entry
also shares a single publication date. There is no per-entry recency signal
anywhere in the file.

### The verdict on M3

**Freshness cannot be calculated from this data.**

Freshness asks how old the information in an entry is, and what would trigger a
re-check. `operational_date` answers a different question: when the system
started running. A system operational since 2019 may have had its entry reviewed
last week or never, and the register cannot tell the two apart.

Building a freshness toggle on `operational_date` would present the age of a
system as though it were the age of its record. That is not a caveat problem. It
is the wrong measurement.

This outcome was anticipated in the brief: if the data has no reliable date
fields, say so and show stage only.

## 30. Phase 3 review findings (owner's ruling of 23 September 2026: fail)

### Review packs were stale

Both packs were generated before the commercial-only re-run and showed
over-scrubbing that no longer existed in the data. The sample pack predated the
current derived file by about ninety minutes. Both have been regenerated from
current data.

**Process change:** review packs are generated in the same run that writes the
derived file, never separately, so they cannot drift from what they describe.

### The literal string "nan"

Checked in both files with default missing-value handling switched off.

| File | Cells holding the literal text "nan" |
|---|---|
| Source | **0** |
| Derived | **0** |

The string was introduced by the pack-rendering script, which converted a
missing value to text for display. The pipeline and the published data are
unaffected, and no completeness figure changes. The rendering defect is fixed:
missing values now render as "(empty)".

### Surface-form matching, and what it missed

Terms were matched as exact contiguous strings. Two consequences, with the same
root cause:

1. A product written "OpenAI" in the blocklist was not matched when written
   "Open AI" in the data.
2. The same product was replaced in one field and left in another field of the
   same row, because the two fields wrote it differently. One case had it
   contiguous in one field and split by punctuation in a use case title.

| Rows where the same term was matched in one field and missed in another | Count |
|---|---|
| Under exact surface-form matching | **5** |
| Under variant-tolerant matching | **2** |

Matching now tolerates spacing, punctuation and casing, and splits camel case,
so a term written as one word also matches when written as two. The same matcher
is used by the scrub and by T2, imported from one place, so the test cannot be
weaker than the fix.

### What variant matching costs

It catches 129 occurrences that exact matching missed, across 45 distinct
written forms. Roughly half are genuine mentions previously missed. The rest are
new false positives, concentrated in terms whose parts are ordinary words once
split.

The three largest new false positives account for about 55 occurrences on their
own: a phrase meaning current, a phrase meaning a helpdesk, and a generic phrase
for searching with AI. These are in the derived data now and are a direct
consequence of the instructed fix. They are the clearest evidence for the
mechanism problem recorded in section 31.

Replacement count moved from 1,339 across 663 rows to **1,437 across 710 rows**.

### Terms checked in context

| Term | Occurrences | On blocklist | What it refers to here | Action |
|---|---|---|---|---|
| A phrase for analysing text | 19 | No | A generic capability, and an internal agency application name | None needed |
| A phrase for consultation responses | 60 | No | Responses submitted by the public during rulemaking | None needed |
| An open-source language | 31 | No | Already retained as a technology descriptor | None needed |
| A government case-management system | 16 | **Yes** | A federal immigration case system, appearing mostly as an authorisation-to-operate system name | **Removed** |
| A procurement assistant | 5 | **Yes** | Described in the data as part of a paid subscription service and named in the vendor field | **Not removed.** Evidence indicates a commercial product. Referred back to the owner |

### Blocklist terms that are government systems rather than commercial products

Method: the same context inspection used for the held-back terms.

| Measure | Count |
|---|---|
| Blocklist terms sourced only from the authorisation-to-operate system name field | 215 |
| Of those, terms that actually match free text | **69** |
| Replacements those 69 cause | 274 |
| Of the 69, government or agency system names | **about 39** |
| Of the 69, genuine commercial products | about 25 |
| Of the 69, generic descriptors that are neither | about 5 |

The remaining 146 of the 215 are long descriptive system titles that never match
running text, so they are noise on the list rather than a scrubbing problem.

## 31. Blocklist rebuilt under option C then B

Full ruling in `governance/decision-rules.md` section 15. Published method and
counts at `data/derived/blocklist_method.json`.

| | Previous mechanism | Now |
|---|---|---|
| Terms on the blocklist | 891 | **645** |
| Replacements made | 1,437 | **1,184** |
| Rows affected | 710 | **604** |
| Firing terms that are government system names | **39** | **0** |

### What changed, in order

1. **Source restricted.** Candidates now come only from the field where an
   agency names its vendor, plus the product column of the consolidated file.
   The field naming an agency's own authorised system is no longer a source.
2. **Genuine products recovered.** The terms option C dropped were filtered to
   the 49 that actually appear in narrative text, each inspected, and 14
   commercial products added back by hand.
3. **Remaining terms classified.** Every term that appears in narrative text was
   inspected in context. Eight were removed: five government or agency systems
   that an agency had entered in the vendor field, and three ordinary words or
   technical terms, including a statistical method and the ordinary expression
   for round-the-clock availability.

### Government system names were corrected, not tolerated

Replacing a federal system name with `[product]` asserts that a public system is
a commercial product. That is a false statement about the data.

Under the previous mechanism 39 firing terms were government or agency system
names. **The count is now zero.**

### Catches that depended on camel-case splitting, held for a ruling

Camel-case splitting was removed. It produced about 55 false positives on its
own, including the ordinary phrases for being current and for a helpdesk, which
between them accounted for 34 occurrences.

Removing it also loses a small number of genuine catches that no other rule
recovers. These are **held for a separate ruling** and are not currently
scrubbed:

| Written form in the data | Occurrences | What it is |
|---|---|---|
| A major model provider's name written as two words | 5 | The spaced form of a one-word company name |
| A copilot product written with a hyphen | 3 | Across two vendors |
| A workflow vendor's name written as two words | 1 | The spaced form of a one-word company name |
| A chat model written with a hyphen | 1 | The hyphenated form |
| A presentation product written as two words | 1 | The spaced form |

**This gap is now closed, and not by reinstating the rule.** On 23 September 2026
the owner directed that each written form be added as its own blocklist term,
using the exact form found in this file and adding no speculative variants.

Six forms were examined. Two needed no term, because existing entries already
covered them case-insensitively. Adding them would have been redundant rather
than protective. The other four were each checked against the narrative text
first, and each produced only genuine commercial references and no false
positives before it was allowed to land.

| | |
|---|---|
| Forms examined | 6 |
| Terms added | **4** |
| False positives introduced | **0** |
| Occurrences of any of the six forms remaining in the derived data | **0** |

Replacements moved from 1,184 across 604 rows to **1,194 across 607 rows**.

Camel-case splitting stays removed. The four terms are exact written forms
observed in this file, so re-downloading the source requires re-checking them
rather than assuming they still apply.

## 32. Review pack generation

Both review packs are now written **in the same run that writes the derived
file**, from the same in-memory data. They cannot describe a version of the data
that no longer exists.

The earlier packs were generated separately and had drifted by about ninety
minutes, which produced a review of over-scrubbing that had already been fixed.

### Terms reviewed and settled, not to be reopened

These three were raised from the stale pack. Each has been checked against
current data and each is correct as it stands. **No action is required and none
should be taken later.**

| Term | Occurrences | Status |
|---|---|---|
| A phrase meaning the analysis of text | 19 | Never on the blocklist. A generic capability and an internal application name. Correct as is |
| A phrase meaning responses submitted during consultation | 60 | Never on the blocklist. Correct as is |
| An open-source programming language | 31 | Never on the blocklist. Retained deliberately as a technology descriptor | 

The procurement assistant raised alongside them **stays on the blocklist**. The
owner confirmed on 23 September 2026 that two vendor-field mentions and a
description of a paid subscription are sufficient evidence that it is a
commercial product.

## The agency submission count: a failure to reconcile, and what was tried

**Recorded 30 September 2026, on the owner's ruling that an honest failure to
reconcile is a better finding than a number with no working.**

The source states **56 total agency submissions**. This project previously
published **54** beside it. That 54 was typed into `src/measures.py` and was
never computed from anything. No method reproduces it. It has been removed.

### Every method attempted

| Method | Result |
|---|---|
| Distinct agency codes in the individually reported file | 41 |
| Distinct agency names in the individually reported file | 41 |
| Distinct agency names in the consolidated file | 45 |
| The two counts added | 86 |
| Union of agency codes with consolidated agency names | 86 |
| Union of agency names, exact strings | 57 |
| Union of agency names, case and punctuation normalised | 57 |
| Union after also folding common title words (the, of, for, United States, Board, Governors) | 52 |

**None gives 56.**

### Why it cannot be settled from the files

The two files use different naming conventions for the same agency. Five pairs
are visible by inspection alone:

| In the consolidated file | In the individually reported file |
|---|---|
| Department of Treasury | Department of the Treasury |
| Federal Reserve Board of Governors | Federal Reserve Board |
| National Endowment of the Arts | National Endowment for the Arts |
| United States Election Assistance Commission | Election Assistance Commission |
| United States Office of Special Counsel | Office of Special Counsel |

The individually reported file also carries an agency code column; the
consolidated file does not, so the two cannot be joined on a key. Any count of
distinct submissions therefore depends on a matching rule, and the source does
not publish one. Choosing a rule would manufacture a figure rather than read
one.

**What the site now shows:** the published figure of 56, and in place of a
counterpart, the words "could not be reconciled", with this note beside it. No
number is published that this project cannot recompute.
