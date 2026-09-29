# Decision rules

The rules the owner sets for this project, in the owner's own words.

These are governance decisions, not technical ones. Most are made in Phase 4,
after the data has been profiled and before any analysis runs. The analysis then
applies whatever is written here.

Status: sections 1 to 3 are empty and belong to Phase 4. Section 4 was decided
by the owner on 22 September 2026 and is binding now.

---

## 1. Unit of registration (M1)

**The question:** when the same AI capability appears more than once in the
register, does that count as one use case or several?

Why it matters: every count on the site depends on the answer. Two people using
different rules will report different totals from the same file, and both will
be correct under their own rule. Stating the rule is what makes a number
readable.

**Owner's rule, 23 September 2026.**

**One row is one use case.** The publisher's own unit is kept, so every number
reconciles with what the source states. No entries are merged.

Entries resembling another are labelled **"candidate duplicates, not
confirmed"**. They are flagged, never merged, and never subtracted from a total.

**All three similarity thresholds are published together**, never one: 120
entries at 0.95, 234 at 0.85, 354 at 0.70. That the flagged population triples
on the choice of threshold is itself a finding about the method. Publishing a
single number would hide that the number is a choice.

**The consolidated route is always presented beside the headline**, and the two
are **never summed**. The stated reason travels with them:

> The published figure of 3,611 counts none of the consolidated route, and the two routes use different units, so a total of the two would be meaningless.

**Why the owner chose it:** merging is the only option that changes a published
total, and it would buy a small correction at the price of a merge that cannot
be defended entry by entry. Flagging shows the reader where the count may
overstate without asserting something the data cannot support.

## 2. Freshness rule (M3)

**The question:** how long may an entry go without verification before it is
treated as stale?

Why it matters: a register that is never re-checked describes the past, not the
present. A freshness rule turns "we have a register" into "we know how current
it is".

**Owner's rule, 23 September 2026.** Freshness cannot be calculated from this
data and no freshness rule is set. The finding replaces the metric, under
section 14.

## 3. Re-check triggers

Events that should prompt an entry to be verified again, regardless of the
calendar.

**Owner's rule, 23 September 2026.** This is a statement of method, not a
recommendation to anyone. It records the conditions under which **this owner**
would treat a register entry as requiring re-verification. It is not published
as advice, and the site does not carry it. See section 14.3.

An entry would require re-verification when any of the following changes:

1. The owner of the system, whether the responsible office or the accountable
   official.
2. The model or its version, including a change of underlying provider.
3. The data sources the system draws on.
4. The scope of what the system is used for.
5. The degree of autonomy with which it acts, including any change to whether a
   person reviews its output before it takes effect.

**How the triggers are used, decided 23 September 2026.** They are not published
as a recommendation. They are used as a **diagnostic of the register**, which is
description rather than advice: for each trigger, report what the register
records.

The five are reported in **two groups**, because they are not the same kind of
absence and merging them would understate the second.

**Group one, four triggers.** Owner of the system, model or version, data
sources, and scope of use. Fields touching each of these exist. **None records a
change, a date of change, or a prior value.**

**Group two, autonomy, reported separately.** The degree of autonomy with which
a system acts is **not present in the 2025 field set**. No field touches it at
all.

"No field records a change" and "no field exists" are different statements, and
the second is the stronger and more accurate one for autonomy.

**Wording:** the autonomy point is stated as **"not present in the 2025 field
set"**. Not as the question having been removed or dropped, which would
attribute an act to someone. This is the case the wording preference in section
12.9 exists for.

---

## 4. Category definition change between years

**Owner decision, 22 September 2026. Binding on Phase 2 onward.**

### The finding

The serious category was **rewritten, not renamed**.

- 2024 followed OMB memorandum **M-24-10**, which used two separate categories,
  **rights-impacting** and **safety-impacting**.
- 2025 follows OMB memorandum **M-25-21**, which uses a single category,
  **high-impact**.

Both years share the same core test, whether the AI output serves as a
**principal basis for a decision or action**. Coverage differs around that
shared core:

- 2024 safety-impacting covered climate and environment.
- 2025 high-impact adds strategic assets, high-value property, and sensitive or
  classified information, and carries a shorter list of presumed categories.
- 2025 introduces a status of **presumed high-impact but determined not
  high-impact**, which has no 2024 equivalent.

**The 2024 and 2025 counts measure different things.** They are not two readings
of one ruler.

Plain-language term. **Definition drift** is what happens when the rule for
counting something changes between two periods. The number moves, but the thing
being counted also moved, so the difference cannot be read as change in the
world. It is one of the most common ways a register misleads an honest reader.

### Scope of impact

| Measure | Affected | Why |
|---|---|---|
| M1 unit of registration | No | Does not use the category |
| M2 completeness and reconciliation | **Yes** | Compares the two years directly |
| M3 freshness | No, but see below | Definition drift is cited in the README as an example of why freshness starts with definitions |
| M4 obligation output | **No** | Uses 2025 data and the 2025 definition only |
| M5 register design comparison | No | Compares OMB with Ontario, not year with year |
| Headline hook | **Yes** if either candidate pair places the two years side by side |

### Rules that now bind the analysis

1. The 2024 and 2025 category counts are **never presented as a trend**.
2. If any output would place the two counts **in the same sentence, the same
   table row, or the same chart**, work stops and the owner is asked first.
3. Trend verbs are banned across the whole repository, not only for this
   category. See section 5 below for the reasoning and the list.

### Analysis that is allowed

Permitted **only if** use case identifiers prove comparable across years. If
they do not, work stops and the owner is told.

- For use cases present in both years, compare the 2024 flag against the 2025
  flag at the level of the individual entry.

This is a crosswalk, not a trend. It describes what happened to specific
entries, not to a population.

**Mandatory caveat, reproduced verbatim wherever this appears:**

> A change in classification may reflect the new definition or an agency reassessment. The data cannot separate the two.

### Required output in View 2

A short note, shown on the page rather than tucked behind a click, recording
that the category definition changed between years. Framed as definition drift:
the rule itself changed, not only the entries.

### Required output in the README

The definition drift note is linked to M3 as a worked example of why comparing
registers over time begins with checking definitions rather than counts.

### Phase 2 tasks this creates

1. From **both** data dictionaries, record exactly how each year codes the
   category: field names, allowed values, and how the "presumed high-impact but
   determined not high-impact" status appears in the data.
2. Record both definitions, with their memo references, in
   `governance/data-provenance.md`.
3. Confirm whether use case identifiers are comparable across years. If they are
   not, stop and report, because the permitted crosswalk above depends on it.

---

## 5. Global ban on trend framing

**Owner decision, 22 September 2026.**

### The reasoning

No count in this project is a safe trend, including the totals. Inclusion
criteria changed between years, consolidated off-the-shelf reporting is new in
2025, and the serious category was defined under a different memorandum in each
year. Any sentence describing movement between two annual figures asks the
reader to believe the ruler stayed still. It did not.

### The list

Banned across the repository, matched as whole words and case-insensitively:

increased, decreased, rose, fell, doubled, grew, growth, jump

### Exemptions

Three files are exempt, because they exist to state the rule:

- `tests/test_banned_words.py`
- `CLAUDE.md`
- `governance/decision-rules.md`

`governance/safeguards.md` is **not** exempt. It documents the ban by pointing
at this file rather than repeating the list, so that it remains subject to the
rule it describes.

### The limit of the test, and what covers it

A word test cannot catch meaning. A sentence can imply a trend without using any
banned verb. Phase 7 therefore includes a **manual trend-framing review**: every
published sentence that mentions more than one year is read for implied
comparison. Recorded in `governance/safeguards.md`.

## 6. Carry-forward analysis (M2)

**Owner decision, 22 September 2026.**

The carry-forward analysis runs. The ban in section 4 covers the category counts
only.

**Amended by section 9.2 on 22 September 2026.** The entry-level crosswalk
between years is dropped, because the 2024 file carries no identifier. What
follows still governs the consolidated off-the-shelf check within 2025.

Before any 2024 entry is labelled **"not carried forward, reason not stated in
the data"**, it must also be checked against the **2025 consolidated
off-the-shelf file**. That reporting category is new in 2025, so an entry that
was individually reported in 2024 may have been folded into a consolidated
submission rather than dropped.

**Record how many 2024 entries matched there.** That number is published
alongside the not-carried-forward figure, because it is the main reason the
not-carried-forward figure would otherwise overstate the case.

The mandatory caveat from the brief still applies wherever the
not-carried-forward number appears: agencies are permitted to drop prior entries
that no longer meet the inclusion criteria, and the research and development
scope changed between years, so a missing entry is not evidence of anything
wrong.

## 7. The three-state category (superseded by section 9.3)

2025 carries a status of **presumed high-impact but determined not
high-impact**, which makes the category three-state rather than yes or no. Who
belongs in the M4 subset therefore has to be decided, and the count changes
either way.

**Superseded.** The owner decided this on 22 September 2026, ahead of Phase 4,
once Phase 1 produced the counts. The rule is in section 9.3. The field turned
out to be four states, not three: 426 rows carry no classification at all.

**Phase 2 must report, as input to that decision:**

1. How many entries carry the presumed-but-determined-not status.
2. Whether a justification field exists for those entries.
3. How often that justification field is filled.

**Owner's likely direction, recorded as a signal and not as a decision:** the M4
main subset is high-impact only, with a separate and clearly labelled band for
the presumed-but-determined-not entries. That band uses **the data's own label
for the status**, not a label invented by this project.

## 8. Headline hook constraints

The headline is two real computed numbers that disagree. Candidate pairs are
brought to the owner after Phase 5. The owner picks.

Excluded from the candidate pool, both for the same reason:

- Any pair built on the **two years' category counts**.
- Any pair built on the **two years' totals**.

In both cases the definitions moved between the years, so the disagreement would
be an artefact of the rules rather than a finding about the data.

The carry-forward pairing suggested in the brief is **no longer available**. The
crosswalk it depended on was dropped under section 9.2.

**Candidate added by the owner, 22 September 2026:** 3,611 entries, 445 flagged
high-impact, 426 with no classification recorded. All three figures come from
one file at one moment, so no cross-year definition problem arises.

## 9. Reconciliation findings, the crosswalk, M4 bands and M5

**Owner decisions, 22 September 2026. Binding.**

### 9.1 How the three unreconciled figures are published

All three are published as findings. Every candidate explanation is stated and
none is chosen.

Each is framed as **a disagreement between a published figure and the data as
published**. Never as an error by the publisher. The publisher is not the
subject of the finding. The data is.

For the consolidated COTS figure specifically, the finding must state that the
README's own per-agency table and the data file agree with each other at 45, and
that only the summary bullet differs.

Drift was tested and ruled out before publication. The data files have not
changed since 14 April 2026, the summary was written the same day, and the only
later edit touched no figure. Recorded in `data-provenance.md` section 3.1.

### 9.2 The entry-level crosswalk is dropped

No name-plus-agency matching is substituted for carry-forward conclusions.

**The cause is published as the finding:** the 2024 inventory carries no unique
identifier, so entries cannot be tracked between years. Paired with the fact
that 2025 introduces an `id` field and instructs that a use case keep the same
identifier across years, so tracking becomes possible from 2025 onward.

Published alongside it, because it is true and material: the 2025 `id` field is
filled on 80.5% of rows and 13 values appear on more than one row. Tracking
becomes possible in principle before it becomes reliable in practice.

A methods note quantifying why name matching was rejected is permitted and is
recorded in `data-provenance.md` section 14. It draws no conclusion about
missing or carried-forward entries.

### 9.3 M4 subset rule, decided now rather than in Phase 4

The M4 subset is **the 445 labelled high-impact only**.

| Band | Rows | Treatment |
|---|---|---|
| High-impact | 445 | The M4 subset |
| Presumed High-Impact, but Not High-impact | 110 | A separate, clearly labelled band. `HI_justification` fill rate reported |
| Classification not recorded | 426 | A third band, labelled "classification not recorded". **No inference in either direction** |
| Not High-impact | 2,630 | Outside the subset |

Bands use the data's own label for the status, not a label invented here.

View 3 must show that 445 + 2,630 + 110 + 426 = 3,611, so the reader can see the
whole file is accounted for and nothing has been quietly dropped.

### 9.4 M5 stands as written

Ontario is **one schema comparison table inside View 2**. Never its own view.
No third register.

The three-row count is stated openly in the text rather than managed around.
The comparison is of **fields asked**, never of volume.

### 9.5 Department of War

Recorded as a scope limit in the README. No carry-forward consequence, because
the agency did not report in 2024 either. The 2024 inventory excluded Department
of Defense use cases by the same mechanism.

## 10. Phase 2 rulings

**Owner decisions, 22 September 2026.**

### 10.1 The withheld overlap figure

The name-matching overlap figure stays withheld from everything published.

**Reason, recorded as required:** the method cannot support the reading the
number invites. The key is not unique within a single year, so the match is not
one-to-one in either direction, yet the figure presents as a carry-forward rate.
A caveat does not survive being quoted. The number would be lifted out of its
paragraph and repeated without it, and at that point the project would have
published a carry-forward rate it had explicitly declined to calculate.

The README's process section records that a number was produced, judged
unpublishable, and escalated to the owner rather than published or discarded.
Discarding it would have hidden a judgment call. Publishing it would have made
the judgment pointless.

### 10.2 The rows carrying a conditional field outside its condition

This becomes a **primary finding**, not a footnote.

Wording rules, binding:

1. Framed as **data against dictionary**. The comparison is between what the
   file contains and what the dictionary describes. Never as conduct.
2. Clustering is reported as an **observation only**. No explanation is offered
   for why some submissions show the pattern and others do not.
3. **The 1.1% fill rate for the high-impact band never appears without the
   dictionary explanation in the same paragraph.** The figure was 1.3% before
   the placeholder scan; the rule attaches to the current figure. The field is specified to
   appear only for the presumed-but-determined-not band, so a low rate in the
   high-impact band is the specification working, not an absence of diligence.
   Separating the two sentences would invite exactly the wrong reading.

### 10.3 Headline candidates, reordered

**Now ranked first:** 3,611 entries, **706 with no usable identifier**.

Published with it: two of those rows carry "TBD" in the identifier field rather
than leaving it blank. The figure was 704 before the placeholder scan.

Published with it, in the same block and not as footnotes:

- 13 identifier values repeat across 28 rows.
- The dictionary asks that a use case keep the same identifier from year to year.
- The dictionary permits agencies to remove the identifier column from their own
  public inventories.

**Ranked second:** 3,611 entries, 445 flagged high-impact, 426 with no
classification recorded.

### 10.4 File encoding as a published finding

The 2024 v2 file is cp1252, not UTF-8. This is published as a finding about
**reusability**, not kept as a technical note in provenance.

The point for a reader: a register that is published for reuse is only reusable
if it can be opened. Read with the assumed encoding, this file raises an error
rather than showing different characters, which reads as a damaged file rather
than a different convention.

### 10.5 What Phase 2 must report

Alongside the field mapping and the identification of contact fields:

1. Which fields the dictionary marks conditional, and the fill pattern of each
   against its stated condition.
2. Which of the 36 fields in 2025 have no equivalent among the 62 in 2024.
3. The reverse: which 2024 fields have no 2025 equivalent.

## 11. The 2024 inventory is a schema reference, not a dataset

**Owner decision, 23 September 2026. Binding on every later phase.**

The 2024 inventory is reclassified. It is **a schema reference**, not a data
source.

### Its only permitted use

The field-set comparison: which questions each year asks. Nothing else.

### Explicitly out of scope, permanently

- No row-level use of 2024 anywhere
- No counts compared between years
- No entries matched between years
- No completeness figures for 2024, and none compared across years
- No category comparison between years
- No headline built on 2024

### Why

The two years cannot be placed side by side at row level. The category was
rewritten under a different memorandum, inclusion criteria changed, consolidated
off-the-shelf reporting is new in 2025, and the 2024 file carries no identifier.
Every one of those is enough on its own. Together they mean any row-level
comparison would describe the rules rather than the world.

Reclassifying the source removes the temptation structurally, rather than
relying on each later phase to remember the reasoning.

### Still published, because they concern the repository and not the rows

Two findings survive the reclassification, since neither makes a claim about any
entry:

1. The file is published as cp1252 rather than UTF-8, so it raises an error
   rather than opening under the common assumption.
2. The repository publishes two files with near-identical names. Its own file
   listing names the one whose row count does not match its stated total.

Both are findings about **reusability**: whether a register published for reuse
can actually be picked up and used.

### The withheld overlap figure

**Permanently out of scope**, not withheld pending a decision. It was produced
by matching 2024 rows to 2025 rows, which section 11 now forbids outright. There
is no future phase in which it becomes publishable. Recorded in
`data-provenance.md` section 14.

### Added to the stop-and-ask list

Stop and ask the owner before doing any of the following:

- Reading 2024 rows for any purpose other than listing its field names
- Producing any figure that pairs a 2024 number with a 2025 number
- Reintroducing the crosswalk, the carry-forward comparison or the overlap
  figure under any name

## 12. Phase 3 rulings

**Owner decisions, 23 September 2026.**

### 12.1 T2 exemptions

T2 keeps scanning **all files**, including markup, attributes and URLs. There is
**no categorical exemption** for markup, attributes or rendered text. Vendor
names appear in `alt`, `title` and `aria-label` attributes and in link URLs, and
one was found inside a link during this phase.

Exempt by exact string only:

| Exact string | Reason |
|---|---|
| `<meta charset` | Required HTML declaration. One company shares the tag name |
| `<meta name="viewport"` | Required HTML declaration for mobile rendering |

Each exemption is recorded in `governance/safeguards.md`. **Adding any further
exemption requires the owner's approval and is a stop-and-ask condition.**

### 12.2 Term list scope

The 2025-only reading stands. There is no gap: S2 protects published data,
published data is 2025 only, so a vendor named exclusively in 2024 never reaches
anything published.

The list may be supplemented with a **manual list of common commercial AI vendor
and product names**, which is not 2024 row data.

### 12.3 What qualifies as a vendor term

S2 targets **commercial companies and their commercial products**.

A term qualifies for the list only if all three hold:

1. It is a proper noun.
2. It is not a controlled-vocabulary value.
3. It is not a multi-word generic phrase.

**Open-source languages, runtimes and general-purpose libraries used as
technology descriptors are retained**, not scrubbed. They describe the
technology used rather than identifying a commercial supplier. The retained list
is published at `data/derived/open_source_terms_retained.json`.

### 12.4 Scrub review pack

Two parts, both reviewed by the owner before Phase 3 closes:

1. Twenty random scrubbed rows.
2. The **twenty most frequently replaced terms, with three before-and-after
   examples each.** Systematic over-scrubbing concentrates in the most frequent
   terms and random rows will not surface it.

### 12.5 Undocumented columns

Proceed using `agency` and `agency_name`, recorded as a documented gap and as a
one-line finding: the file carries 36 columns, the dictionary documents 34.

Confirmed before relying on them: the two map **one-to-one in both directions**,
41 codes to 41 names, no code with multiple name spellings, no name with
multiple codes, and no variants differing only by whitespace or case. No
clustering count needs restating.

### 12.6 The empty-list finding

Published as a finding in the same class as the encoding finding, framed as
**reusability**. Naive and corrected figures shown side by side. States plainly
that standard tools read the two-character text as content.

### 12.7 Placeholder scan

Every text field is scanned for values behaving as empty. Each is added to the
empty-value rule and every completeness figure is recomputed.

**One distinction the scan forced**, recorded because it changes figures: a
value is only an absence in a field that expects written content or a URL. In a
multiple-choice field the same string can be a valid selection. The dictionary
lists "b) Not applicable" as an allowed answer to two oversight questions, so
there it is an answer and is counted as filled.

### 12.8 Oversight-block wording

Describe **the shape only**: the nine fields are answered together or not at
all, 126 rows all, 317 none, 2 partial. Offer no explanation and imply none.

Two caveats travel with it wherever it appears:

> A filled field shows that information was provided, not that the practice is adequate.

> The pattern describes what reached the file, not the oversight practice itself.

### 12.9 Banned list: closed

**Base forms only, as applied on 22 September. Nothing added.** Specifically
**not** added: "dropped", "removed".

Recorded instead as a **wording preference**, checked manually in Phase 7:

> Prefer "not present in the 2025 field set" over "dropped" or "removed" when comparing field sets.

**The principle, recorded because it governs future requests:** a banned word
list that expands to cover judgment calls stops working as a control and starts
costing clarity. A list catches words. It cannot catch meaning, and pretending
otherwise makes it both weaker and more annoying.

## 13. The placeholder rule

**Owner decision, 23 September 2026. Binding.**

A value that looks like a placeholder is read according to the **type of field it
sits in**, and the dictionary's allowed values decide which.

| Field type | How a placeholder value is read |
|---|---|
| Free text, or a field expecting a URL | **An absence.** "No", "Not available", "TBD", "Not applicable" in a field expecting written content or a link record that there is nothing to give |
| Multiple choice | **Possibly an answer.** If the dictionary lists the value among the allowed selections, it is an answer and counts as filled |

The dictionary is the authority, not the appearance of the string.

**The case that forced the rule:** the dictionary lists "b) Not applicable" among
the allowed selections for the appeal-process and fail-safe questions. Read as an
absence, those two fields would have moved from 28.8% to 26.5% and 22.0%, and the
oversight-block finding would have been broken on a mistake.

This is published as a finding in its own right. It belongs to the same class as
the empty-list finding and the encoding finding: all three are ways a published
register can be counted wrongly by someone doing the obvious thing.

## 14. M3 rulings

**Owner decisions, 23 September 2026. Binding.**

Freshness cannot be calculated from this data. The register records no
verification date, no update date and no review date, and the only date field
records when a system became operational rather than when its entry was checked.
Evidence in `data-provenance.md` section 29.

### 14.1 The finding replaces the metric

M3 reports that the register cannot express how current any entry is, because it
records no verification date. The gap is the finding.

### 14.2 View 1

The freshness toggle becomes a **development-stage filter**, which is real data.

The filter carries, on the filter itself and not in a footnote:

> Stage is not recency. A stage describes where a system is in its life, not when this entry was last checked.

It also carries its own coverage, so the replacement does not inherit a coverage
problem silently:

| Measure | Value |
|---|---|
| Rows carrying a stage | 3,273 of 3,611 (90.6%) |
| Rows with no stage recorded | **338** |

The placeholder scan did **not** change this count. No value in this field
matched the empty-value rule, because the field is multiple-choice and its four
allowed selections are all substantive. 338 before the scan, 338 after.

### 14.3 The operational-date distribution

Appears as **context only**, labelled as time since systems became operational,
**never** as entry age, and always shown against its coverage of 31.7% of rows
so that nobody reads it as describing the register as a whole.

### 14.4 Re-check triggers are not published as a recommendation

This project describes what registers do. It does not argue what they should do.

That ruling is why M5 stayed scoped to comparing the fields each register asks,
and why the absence of the autonomy question was reported rather than elevated
into an argument. Publishing re-check triggers as a design recommendation would
break it visibly.

The triggers are therefore recorded in section 3 of this document as the
**owner's own rule of method**, stating the conditions under which this owner
would treat an entry as requiring re-verification. The site reports the finding
only. The README's limits section may state that the design question is left
open.

## 15. The blocklist mechanism

**Owner decision, 23 September 2026. Option C, then B. Binding.**

### The problem being solved

A term earned its place on the blocklist from how it appeared in a field where
an agency names a supplier, and was then applied to every field. Those fields
are where suppliers are named. The narrative fields are where the same word may
be ordinary English, or the name of the agency's own system.

### Option C: restrict the source

Candidate terms are taken **only from the field where an agency names its
vendor**, and from the product column of the consolidated file. The field where
an agency names its own authorised system is no longer a source.

Terms that option C drops are not simply lost. They are filtered to those that
actually appear in the narrative text, and the genuine commercial products among
them are **added back by hand**. The loss of real products is not accepted as a
cost of the change.

### Option B: classify what remains

Every term that actually appears in the narrative text is inspected in context
and classified commercial or not. The reasoning is published per category at
`data/derived/blocklist_method.json`. Terms that never appear in narrative text
need no inspection, because they can cause no replacement.

### Government system names are errors, not noise

Replacing a federal system name with `[product]` **states something false about
the data.** It presents a public system as a commercial product. That is a
wrong assertion, not untidiness, and it is corrected rather than tolerated.

| | Firing terms that are government or agency system names |
|---|---|
| Under the previous mechanism | **39** |
| After option C | 5 |
| After option B inspection | **0** |

### Option A was not implemented

Field-type-aware application of one blocklist. Elegant, and consistent with the
placeholder rule, but its hard part is a defensible test for what counts as
ordinary English, and the project would then have to defend that test. Option B
makes the same judgment explicit for each term instead of hiding it inside a
heuristic.

### Why option D was rejected

Option D was to keep the existing mechanism and add exceptions as each review
turned them up. It was refused.

The decisive objection is that **it has no natural stopping point**: the
mechanism generates the cases, so each review surfaces more, and the exception
list grows for as long as anyone keeps looking.

Before this ruling the project had already accumulated nine held-back terms,
three restorations after evidence, two casing carve-outs and three test
exemptions, none of them wrong individually. That is option D happening without
anyone having chosen it.

**The full argument is written up in the README process notes**, because it is
the most transferable thing this project has produced and it belongs where a
reader will find it. This entry records the decision; the README records the
reasoning.

### Matching: camel case removed

Matching tolerates spacing, punctuation and casing. **Camel-case splitting is
removed.** It made any product whose name is two ordinary words joined together
match those two ordinary words in running prose, producing about 55 false
positives on its own, including the ordinary phrases for being current and for a
helpdesk.

Genuine catches that depended on camel-case splitting alone are named in
`data-provenance.md` section 31 and **held for a separate ruling**. They are not
recovered by keeping the rule.

## 16. Phase 3 closure

**Owner decisions, 23 September 2026. Phase 3 closes.**

### 16.1 URLs containing a blocklist term

Option 2. The **whole URL is replaced** and what it was is kept, named from the
column it sat in: a code repository, a data source, or a privacy impact
assessment.

Scrubbing only the host leaves something shaped like a working link, which a
reader may try, cite, or take as evidence the link was checked. Replacing the
whole URL removes that. Naming the kind of link preserves the fact that the
entry supplied one, which the completeness figures depend on.

### 16.2 Names found by the narrative search

All seven commercial names found in the narrative fields were added as
individually reviewed terms, together with the two manufacturer names appearing
in use case titles, and the three product lines belonging to one of those
manufacturers. Twelve terms in total, each checked for ordinary-word collisions
before it landed. None had any.

Two candidates were **not** added, on the analysis that one is an open-source
project already covered by the retention rule and the other is a federally
funded research project whose acronym resembles a product name.

### 16.3 No further scrub review cycles

**This is the last one.** Any vendor name found later is recorded in
`data/derived/known_issues.json` with its location, and fixed only if the fix
costs nothing.

No further passes are run over the narrative fields. The scope limit already
recorded in `governance/safeguards.md` and in the README covers exactly this
case, and continuing to search would contradict the argument that refused the
patching approach. An obligation with no natural endpoint is not a control.

**The scrub is a safeguard, not a deliverable.** It has taken a disproportionate
share of this project's attention, and the findings the project exists to
produce are not built yet.

## 17. Page four: a scope clarification, not a reversal

**Owner decision, 25 September 2026.**

A fourth page will state what the author would build, given what the audit found.
This does **not** reverse the rule that the project describes what registers do
rather than arguing what they should do.

### The boundary

| | |
|---|---|
| **The descriptive rule governs** | Claims about the registers. This project does not argue what either publisher should ask |
| **Page four is** | A statement about the author's own design, built from what the audit found |

The distinction is between "this register ought to ask X" and "given what I
found, here is what I would build". The first is advice to a publisher. The
second is the author's own work, offered as their own.

### What holds the line

Three requirements, and they are the reason the page can exist without the rule
bending:

1. **Every point traces to a finding.** A field that cannot be traced to
   something the audit established does not go on the page.
2. **The page states its own limits**: one register, one year, read from
   outside, with no access to how any agency works.
3. **Nothing on the first three views changes to support it**, and no
   recommendation appears anywhere in the findings.

### The standing instruction

**If any line drafted for page four argues what a register should ask, it is
flagged to the owner before it ships.** It is not resolved by reclassifying the
page. The boundary is held line by line, not by the label on the page.

## 18. The dashboard, and the site's entry point

**Owner decisions, 25 September 2026.**

### 18.1 The dashboard becomes the landing page

The dashboard becomes the site's entry point and the register moves to its own
page.

**Sequencing.** Deploy at Phase 9 with the register still at the root. Swap when
the dashboard exists. **The live address is not shared until the swap is
done**, so the root never changes meaning under anyone who has seen it.

The README and the deployment are both written against the final structure, so
neither is rewritten later.

### 18.2 The caveat test

**A figure goes on the dashboard only if its qualification survives being
shortened to a line that still holds.**

A figure that cannot carry its qualification in one line **stays in the site as
normal and is reachable from the dashboard through a link to its section**. It
is not reproduced on the dashboard as a number.

This exists because a dashboard is the artefact this project has spent its whole
length arguing against: a figure lifted away from what qualifies it. The test is
what makes the page safe to build rather than a contradiction of the findings.

**When the dashboard is built, the owner is told which figures passed and which
did not, with the shortened qualification for each that passed.** Anything
uncertain goes to the owner rather than being decided in the drafting.

### 18.3 The dashboard says what it rests on

The dashboard states, in one line, that **each figure links to the working
behind it**, so a reader knows the conclusions rest on something they can check
rather than on assertion.

### 18.4 Internal links are tested

Every internal link on every page must resolve to a page that exists, and a link
carrying a query string must resolve to a page that reads that query string.

**The cross-view links carrying a band filter are updated in the same change as
the rename, never afterwards.** A link to a page that exists but ignores the
query fails silently: no error, no missing page, just the wrong view with the
filter apparently not working.

## 19. "The entries it flags as most serious" is the author's gloss

**Recorded 29 September 2026.**

The register's own term is **high-impact**, defined by the publisher as the AI
output being the principal basis for a decision affecting people.

**"The entries it flags as most serious", and "the riskiest systems", are the
author's plain-English gloss on that term.** They are not the publisher's
wording and no publisher uses them.

### The rule

The gloss is used consistently across all pages, and **the register's own term
appears with it on first use on each page**, so a reader is never given the
plain phrase without the word the source actually uses.

### As built, checked 29 September 2026

| Page | Where the gloss first appears | Where the register's term appears |
|---|---|---|
| The register | In the oversight lead-in | **27 characters earlier**, in the same sentence |
| What the register does not tell you | Not used | n/a |
| If someone asked about the riskiest systems | In the page title | **79 characters later**, in the subtitle directly beneath it |

**One case does not strictly meet the rule and is recorded rather than
smoothed over.** On the third page the gloss stands in the page title, and the
register's term arrives in the subtitle on the next line. Putting the term in
the title itself would make the plainest heading on the site the most technical,
which would undo the readability work that produced it.

The owner is asked to rule on whether a title may carry the gloss with the term
in the line beneath, or whether the title changes.

## 20. The dashboard leads with the design view

**Owner decision, 29 September 2026. Supersedes the ordering in section 18.**

The dashboard's order is:

1. **Framing**, two or three lines drawn from the README: what this is and what
   was examined.
2. **A compact preview of the proposed field set** from page four, shown on the
   dashboard itself rather than only linked, with one line stating it came from
   what the audit found, and a link through to the full page with its two worked
   examples.
3. **The key findings as prominent figures**, each linking into the finding it
   summarises, framed as the evidence the field set rests on.
4. **A link to the README** for the full account of the work.

### The preview stays a preview

A reader should get the shape of the field set at a glance and go to page four
for the detail. **The preview must not become the whole field set.**

### What this changes, and what it does not

The site's entry point now leads with the author's design and presents the
findings as what it rests on. **The first three views remain descriptive**, no
recommendation appears anywhere in the findings, and every figure still loads
from `data/derived`.

### One consequence, recorded because it sits on the boundary this project has been careful about

Framing the findings as evidence for the field set means a reader arriving from
the dashboard meets them as support for a proposal, even though the findings
themselves argue nothing and are unchanged.

That is a change in how the findings are encountered rather than in what they
say. It is recorded here so that the distinction is deliberate: **the ordering
is an argument the dashboard makes, and the findings pages continue not to make
it.** If any later edit lets that framing leak backwards into the findings
themselves, it is a defect and is flagged.

### The README is written to this structure

Its opening supplies the framing lines, so the dashboard quotes the README
rather than restating it in different words.

## 21. Decision log

| Date | Decision | Options considered | Owner's reasoning |
|---|---|---|---|
| 2026-09-22 | Authorship line reads "Governance design by Sana Ahmad." | n/a | Required by S11 in Phase 0 |
| 2026-09-22 | Repository location: `/Users/tigersaa/__CODE/AI Usecase inventory` | Three locations offered | Owner selected a new empty folder |
| 2026-09-22 | `.gitignore` uses `data/raw/*` with an exception for an empty marker file, rather than a bare `data/raw/` | Bare directory rule, or pattern plus exception | Identical protection, and the folder survives a fresh clone |
| 2026-09-22 | Category definition change treated as definition drift. Trend framing banned. Crosswalk permitted only at entry level and only if identifiers match | Trend comparison rejected outright | The two years apply different memoranda, so the counts do not measure the same population |
| 2026-09-22 | Carry-forward analysis runs. 2024 entries checked against the 2025 consolidated off-the-shelf file before being labelled not carried forward, and the match count published | Label without the check | Consolidated reporting is new in 2025, so the unchecked figure would overstate |
| 2026-09-22 | Global ban on eight trend verbs across the repository, three files exempt, plus a Phase 7 manual trend-framing review | Ban scoped to the category only | No count here is a safe trend, and a word test cannot catch implication |
| 2026-09-22 | Three-state category stays a Phase 4 decision. Phase 2 reports the counts and the justification field first | Decide now | The decision needs the numbers underneath it |
| 2026-09-22 | Headline pool excludes pairs built on the two years' category counts or the two years' totals | Allow totals | Definitions moved, so the disagreement would be an artefact of the rules |
| 2026-09-22 | Drift tested before publishing any reconciliation finding, and ruled out by commit history | Publish without testing | A rolling-update source could have moved under us. It had not |
| 2026-09-22 | Three unreconciled figures published as findings, all candidate explanations stated, none chosen, never framed as publisher error | Choose the likeliest explanation | The data cannot separate the candidates, and the subject of the finding is the data |
| 2026-09-22 | Entry-level crosswalk dropped. No name matching substituted. The cause is published as the finding | Name-plus-agency matching | The method is not one-to-one within a single year, so it cannot carry a conclusion |
| 2026-09-22 | M4 subset is the 445 high-impact only, with two further labelled bands and the full arithmetic shown | Fold the presumed-but-not band into the subset | The bands answer different questions and the reader should see all four |
| 2026-09-22 | M5 stands. Ontario is one table inside View 2, three-row count stated openly, fields compared never volume | Drop M5, or give Ontario its own view | The design point does not depend on row count |
| 2026-09-22 | Headline candidate added: 3,611 entries, 445 high-impact, 426 classification not recorded | | Single file, single moment, no cross-year definition problem |
| 2026-09-22 | Overlap figure withheld from all published output, reason recorded, escalation noted in the README process section | Publish with caveat, or discard | A caveat does not survive being quoted, and discarding would hide the judgment |
| 2026-09-22 | Conditional-field mismatch becomes a primary finding, framed as data against dictionary, clustering as observation only | Footnote it | It is the clearest thing the profiling found |
| 2026-09-22 | The 1.3% high-impact fill rate never appears without the dictionary explanation in the same paragraph | State it plainly | Separated, it invites the opposite of the true reading |
| 2026-09-22 | Headline candidate on identifiers ranked first, above the classification blanks | Keep the classification pair first | Identifier absence is the finding with consequences for every future year |
| 2026-09-22 | cp1252 encoding published as a reusability finding | Provenance note only | A register published for reuse has to open |
| 2026-09-23 | 2024 reclassified as a schema reference. No row-level use anywhere. Added to the stop-and-ask list | Keep it as a dataset with caveats | A structural limit cannot be forgotten by a later phase the way a caveat can |
| 2026-09-23 | The overlap figure is permanently out of scope rather than withheld | Leave it withheld pending review | The analysis that produced it is now forbidden, so there is no future in which it is publishable |
| 2026-09-23 | Encoding and the two-file contradiction stay published as reusability findings | Drop them with the reclassification | Neither makes a claim about any entry |
| 2026-09-23 | T2 keeps scanning all files. Two exact-string exemptions only. Further exemptions are stop-and-ask | Categorical markup exemption | Vendor names do appear in attributes and URLs, and one was found in a link |
| 2026-09-23 | Term list stays 2025-only, may be supplemented with a manual commercial AI vendor list | Read 2024 vendor columns | Published data is 2025 only, so there is no exposure |
| 2026-09-23 | S2 targets commercial companies and products. Open-source languages, runtimes and libraries retained and published | Scrub every technology name | They describe technology, not a commercial supplier |
| 2026-09-23 | Review pack adds the 20 most replaced terms with three examples each | Random rows only | Systematic over-scrubbing concentrates in frequent terms |
| 2026-09-23 | Proceed with agency and agency_name, recorded as a documented gap and a finding | Stop until documented | Mapping verified one-to-one in both directions |
| 2026-09-23 | Empty-list finding published as a reusability finding with naive and corrected figures side by side | Footnote it | Standard tools read the two characters as content |
| 2026-09-23 | Placeholder scan run, empty-value rule extended, all completeness recomputed | Keep the Phase 2 rule | Several fields recorded absence as text |
| 2026-09-23 | Banned list closed at the base forms. Wording preference recorded instead, checked manually in Phase 7 | Add "dropped" and "removed" | A list that expands to cover judgment calls stops working as a control |
| 2026-09-23 | Third T2 exemption for the exact geophysics phrase. No case-sensitive subset | Make T2 case-sensitive for some terms | Case-sensitivity fixes one word and opens a systematic hole, since brand names appear lowercased in free text |
| 2026-09-23 | Placeholder rule set by field type, with the dictionary deciding, and published as a finding | One blanket list | A blanket rule would have broken the oversight-block finding |
| 2026-09-23 | Headline candidate updates to 706 with the "TBD" note. Justification rule attaches to 1.1% | | Both figures moved after the placeholder scan |
| 2026-09-23 | Held-back terms published as count, reason and semantic category, with the context evidence. Literal list stays uncommitted. No S2 exception logged | Publish the literal terms | Publishing them would breach the safeguard the file documents, and there is no deviation to record |
| 2026-09-23 | M3: the finding replaces the metric. Stage filter replaces the freshness toggle, carrying its own coverage. Operational dates are context only | Build freshness on operational_date | That would present the age of a system as the age of its record |
| 2026-09-23 | Re-check triggers recorded as the owner's rule of method, not published as a design recommendation | Publish as a recommendation | The project describes what registers do and does not argue what they should do |
| 2026-09-23 | R4 published with the 18.4% unresolvable rate and the five later-dated values as an observation | | The ambiguity cannot be resolved from the file |
| 2026-09-23 | Blocklist mechanism: option C then B. Source restricted to the vendor field, then every firing term classified by hand | Option A, or option D | A makes the project defend a heuristic. D has no natural stopping point |
| 2026-09-23 | Terms dropped by C are filtered to those that fire and the genuine commercial products added back by hand | Accept the loss as a cost of C | The loss of real products is not a necessary price of fixing the source |
| 2026-09-23 | Government system names treated as errors and corrected to zero | Treat as noise | Replacing a federal system name with [product] asserts something false about the data |
| 2026-09-23 | Camel-case splitting removed from matching. Spacing, punctuation and casing tolerance kept | Keep camel case for the catches that depend on it | About 55 false positives from one rule. The dependent catches are named and held |
| 2026-09-23 | The procurement assistant stays on the blocklist | Remove as a false positive | Two vendor-field mentions and a subscription description is sufficient evidence |
| 2026-09-23 | URLs containing a term are replaced whole, with the kind of link named from the column | Scrub the host only | A broken URL that reads as real is worse than an honest gap |
| 2026-09-23 | Twelve reviewed commercial names added; two candidates declined on analysis | Add all candidates | One is open source and already covered, one is a research project acronym |
| 2026-09-23 | No further scrub review cycles. Later findings go to a known-issues file | Keep reviewing | Searching has no natural endpoint, which is the argument that refused patching |
| 2026-09-23 | **Phase 3 closed** | | Tests pass and the owner has reviewed both packs |
| 2026-09-23 | M1: publisher's unit kept, candidates flagged never merged, all three thresholds published, consolidated route always shown beside the headline and never summed | Merge duplicates | Merging changes a published total on a judgment that cannot be defended entry by entry |
| 2026-09-23 | Triggers used as a diagnostic, reported in two groups, autonomy separately as "not present in the 2025 field set" | One group of five | "No field records a change" understates "no field exists" |
| 2026-09-25 | Page four recorded as a scope clarification, not a reversal. The descriptive rule governs claims about the registers; page four states the author's own design | Record it as a reversal | A statement about the author's own design is not a claim about either register |
| 2026-09-25 | Any page-four line that argues what a register should ask is flagged before shipping, never resolved by reclassifying the page | | The boundary is held line by line |
| 2026-09-25 | The LinkedIn carousel is dropped and not carried forward | | Owner decision |
| 2026-09-25 | Dashboard becomes the landing page. Register moves to its own page. Swap happens when the dashboard exists, and the address is not shared until then | Swap at deployment, or never | Deciding now means the README and the deployment are written once |
| 2026-09-25 | A figure reaches the dashboard only if its qualification survives shortening to one line that still holds. Others are linked to, not reproduced | Put every headline figure on it | A figure without what qualifies it misstates the finding |
| 2026-09-25 | Every internal link is tested, including that a query string resolves to a page that reads it | Check by hand at the rename | A link to a page that ignores its query fails silently |
| 2026-09-29 | Withholding-status finding shipped to the oversight section of the third page, not the headline | Make it the headline | The identifier finding stays as the headline on the register page |
| 2026-09-29 | Caveat restated about the field rather than about anyone answering it | "a required question left unanswered" | That wording makes someone the agent who did not answer |
| 2026-09-29 | The gloss on high-impact recorded as the author's own, with the register's term required alongside it on first use per page | Leave it unrecorded | It is the author's wording and reads as if it were the publisher's |
| 2026-09-29 | Dashboard leads with the design view, findings follow as the evidence it rests on | Findings first, design last | Owner decision. The ordering is the dashboard's argument, not the findings' |
| 2026-09-29 | The field set appears on the dashboard as a compact preview, never in full | Link only, or show it all | A reader should get the shape at a glance and go to page four for the detail |

## 21. Four rulings issued together, 30 September 2026

The owner issued these as a block so that nothing stayed open waiting on them.

| Question held open | Ruling |
|---|---|
| View 2's fourth question does not match the section list the owner gave: the oversight question sits on page three, and View 2's fourth section is the counting traps | **Question four stays as drafted**, "Can a careful person count this file correctly?", with the oversight question carried as a linked line beneath the row, pointing at `obligations.html` |
| The five View 2 sections were collapsed by default, which served "clicking a row opens the finding" and defeated "the five read as one continuous argument" | **All five open by default.** A row click scrolls to its section rather than opening it. The summary rows and the side rail are both ways of jumping to a section, not ways of revealing one |
| Whether the completeness-shape figure belongs on the landing page's evidence strip. The developer reported being uncertain rather than deciding | **It stays out and is linked instead. The uncertainty was the answer.** A figure whose qualification cannot be shortened without changing what it says does not go on the strip |
| Two exact-string exemptions would be needed to publish the repository link | **Both approved**, recorded in `governance/safeguards.md` with their reasons and their scope. Exact strings only |

