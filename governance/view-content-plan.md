# Content plan for the three views

Agreed before any markup is written. Every finding is assigned. Nothing is
discovered while writing HTML.

Every figure on every page is loaded from `docs/data/findings.json`, copied from
`data/derived/` (S5). Disclaimer in every footer (S9). The Ontario attribution
appears wherever Ontario data is shown.

---

## View 1. Register (`index.html`)

The site opens here, so the headline sits here.

| Rank | Content | Source |
|---|---|---|
| 1 | **Headline.** 445 entries flagged high-impact, 317 answering none of the nine oversight fields | M4 |
| 2 | **Candidate 1 as a finding in its own right.** 3,611 entries, 706 with no usable identifier | M1, M3 |
| 3 | **The register table.** Searchable, one row per entry, with a completeness indicator per row | M2 |
| 4 | **Development stage filter**, carrying R5 on the control itself | M3, R5 |

**Headline caveats, both on the page, neither behind a click nor in a footnote:**

> A filled field shows that information was provided, not that the practice is adequate. An empty field is not evidence that the practice is absent.

> The pattern describes what reached the file, not the oversight practice itself.

**Never worded as an oversight failure.** The sentence describes what reached the
file. No verb attributes an act to any agency.

**Candidate 1 is stated at the same length as candidate 3 on View 3**, since both
are findings about a field being blank: the pair of numbers, the note that 704
are blank and two hold "TBD", and the note that thirteen identifier values
appear on more than one row. The dictionary's provisions on identifier
continuity stay in provenance.

**R5 sits on the filter control:** 3,273 of 3,611 rows carry a stage, 338 carry
none, and the line "Stage is not recency. A stage describes where a system is in
its life, not when this entry was last checked."

**Per-row completeness indicator** carries the detailed field-by-field figures,
which is why View 2 needs only a summary. See the capacity note below.

---

## View 2. Gaps (`gaps.html`)

| Rank | Content | Source |
|---|---|---|
| 1 | **M1 unit of registration.** All three thresholds, the consolidated route, the never-summed reason | M1 |
| 2 | **M2 reconciliation.** Four figures that match, three that do not, the source table's internal disagreement, and a short completeness summary | M2, R1, R3 |
| 3 | **M3 freshness as a finding.** The two trigger groups | M3, R4 |
| 4 | **The reusability set, R1 to R6**, shown together as one set | R1 to R6 |
| 5 | **M5 register design comparison**, then the vendor observation as its own block | M5 |

**M1 shows all three thresholds together**, never one: 120 entries at 0.95, 234
at 0.85, 354 at 0.70. Labelled "candidate duplicates, not confirmed". The page
states that the flagged population triples on the choice of threshold, so the
number is a choice rather than a property of the register.

**The consolidated route sits beside the headline count**, never summed with it,
carrying its reason verbatim:

> The published figure of 3,611 counts none of the consolidated route, and the two routes use different units, so a total of the two would be meaningless.

**M2 reconciliation.** The four figures that reconcile are **one line**: four of
seven published figures reconcile exactly, with the detail in provenance. They
prove the work is sound, which is provenance's job rather than a page's. The
three that do not reconcile get a short table, with both candidate explanations
stated and neither chosen. Then the source table's internal disagreement of one. Framed as a
disagreement between published figures and the data as published, never as
error by the publisher. For the consolidated figure, the page states that the
source's own table and the data file agree at 45 and only the summary differs.

**R1 and R3 appear inside M2 as counting notes**, because they explain why the
completeness figures are what they are: the two fields recording an empty answer
as a two-character string that standard tools read as content, with naive and
corrected figures side by side, and the rule that a placeholder records an
absence in a text or URL field but may be a valid selection in a multiple-choice
field.

**The reusability set is then shown whole, as rank 4.** R1 to R6 have a shape
that only holds if none is missing: four are values that read too high, one is
an option set that looks exhaustive, and one is a pair of files where both open
correctly and neither can be shown to be the intended one. Removing any of them
for space breaks the set.

R2 and R6 both concern a repository rather than its rows. They were preserved as
published findings by the same instruction that made the 2024 inventory a schema
reference, which restricts row-level use of that data and does not demote
findings about the file itself. R2 is not a finding about 2024's contents: it is
a finding that the file cannot be read correctly with standard tools, which
stands whatever the file contains.

**M3** states that the register cannot express how current any entry is, then
the two trigger groups, reported separately and not merged:

- Four triggers whose fields exist but record no change, no date of change and
  no prior value: owner of the system, model or version, data sources, scope of
  use.
- Autonomy, reported separately: **not present in the 2025 field set.** No field
  touches it at all.

The page states why they are not merged: "no field records a change" and "no
field exists" are different statements, and merging them would understate the
second.

**R4** sits with M3: 38.8% of rows carry a value in the single date field, 81.6%
of those parse, 18.4% cannot be resolved to a century or a day order, and the
ambiguity cannot be resolved from the file. The five values dated later than the
download are an observation with no inference.

**M5** is one comparison table of fields asked, never volume. The page states
openly that the Ontario register holds three entries.

**Then the vendor observation, as its own block and not a line in the table:**

> The Ontario register names no vendor in any published field. The federal register publishes a vendor name field. That field is the one this project removes from its own published data under its safeguard against publishing vendor names.

Stated as an observation. No argument is attached, and no conclusion is drawn
about either register.

**Ontario attribution appears on this page**, with a link to the licence:

> Contains information licensed under the Open Government Licence – Ontario.

---

## View 3. Oversight information pack (`obligations.html`)

| Rank | Content | Source |
|---|---|---|
| 1 | **The four bands**, with the arithmetic shown | M4 |
| 2 | **Candidate 3 as a finding in its own right.** 3,611 entries, 426 with no classification recorded | M4 |
| 3 | **The oversight block shape.** 126 all, 317 none, 2 partial | M4 |
| 4 | **Field coverage** across the nine, for the 445 | M4 |
| 5 | **The presumed band**, with its dictionary note in the same paragraph | M4 |
| 6 | **Downloads.** The export as CSV and Markdown | M4 |

**Bands shown as 445 + 2,630 + 110 + 426 = 3,611**, so the reader can see the
whole file is accounted for and nothing has been quietly set aside. Bands use
the data's own labels.

**The 426 band is labelled "classification not recorded"** with no inference in
either direction.

**The presumed band's justification rate never appears without the dictionary
explanation in the same paragraph:** the field is specified to appear only when
that band is selected, so a low rate in the high-impact band is the
specification working rather than an absence of diligence.

**Framing, on the page:** this is a practice exercise modelled on a realistic
request. It is not a response to a request from any body.

---

## Capacity note: View 2 does not fit as listed

Four sections, five tables and the vendor block is at the limit of a readable
page. Rather than making the page longer, one thing moves.

**What moves:** the full field-by-field completeness table, 33 fields against
two populations. It goes to **View 1 as the per-row completeness indicator**,
which the brief already specifies, and View 2 keeps only a short summary naming
the fields that matter to the other findings.

**What shortens:** R1 and R3 become counting notes inside M2 rather than
standalone findings with their own headings. They explain why the figures are
what they are, which is exactly what a counting note is for.

**What goes to the README instead of a view:** nothing. An earlier draft of this
plan moved R2 there and left the two-file contradiction unplaced. Both stay on
View 2 as part of the reusability set, for the reason given above.

**What was shortened to make room instead:** the four M2 figures that reconcile
become one line, and candidate 1 on View 1 is cut to the length candidate 3 gets
on View 3.

**What does not move:** the three thresholds, the never-summed reason, the two
trigger groups, and the vendor observation. Each was specifically directed, and
each is short.

---

## Presentation change, 24 September 2026

View 2 was unreadable as a single column: six sections, five tables, twelve
qualifications, all on screen at once.

**Sections are now tabs.** One section is shown at a time. The assignment of
findings to sections is unchanged, nothing was removed, and no number changed.

**A qualification is never separated from what it qualifies.** Both sit inside
the same panel, so whenever a finding is on screen its qualification is too.
This preserves the rule that caveats are visible by default rather than behind a
control, but it is a change in what "by default" means on first load, and it is
recorded here as such.

**Colour now carries meaning** rather than decoration: counting sections, gaps,
method notes and the register comparison each have their own accent, used on the
panel edge, the figures and the active tab marker.

Two other things arrived with it. Asset URLs now carry a content stamp, because
three separate rounds of confusion turned out to be a browser serving a stale
file rather than a broken feature. The stamp is rendered with letters only, so
it does not trip the rule against numbers in the markup.

