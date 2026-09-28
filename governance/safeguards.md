# Safeguards

Twelve rules that apply to every file published by this project. Each one has an
automated test in `tests/`. A deliverable that fails any test is not done.

Status legend: **Live** means the test is written and runs. **Stub** means the
test file exists but the check is not implemented yet. Phase 0 creates stubs.
The full suite becomes live from Phase 3 onward.

| ID | Safeguard | How it is enforced | Test | Status |
|---|---|---|---|---|
| S1 | Source attribution | Every source named, linked, dated and hashed in `governance/data-provenance.md`. Sources are never renamed or hidden | Manual review plus T7 | Stub |
| S2 | No vendor or product names | Vendor and product columns dropped. Free-text mentions replaced with `[product]`. URLs containing a term replaced whole. Raw files are gitignored | T2 | **Live, passing** |
| S3 | No agency judgments | No ranking, score, league table or chart comparing agencies. Agency names appear only as published facts in row-level detail | T3 | Stub |
| S4 | Neutral language | Findings describe the data, not the conduct of an organisation. Banned word list in CLAUDE.md Section 8, extended by the banned trend framing in decision-rules.md section 4 | T4 | Stub |
| S5 | Traceable numbers | Every number on the site is computed by the notebook, written to `data/derived/`, copied to `docs/data/` and injected into the page by JavaScript. No number is typed into HTML | T5 | Stub |
| S6 | Reconcile to published totals | Row counts checked against the totals published by the source before any analysis. A mismatch stops the work and is reported to the owner | T1 | Stub |
| S7 | Raw data untouched | Raw files downloaded by script, verified by SHA-256 hash, never edited. All changes happen in derived files | T7 | Stub |
| S8 | No personal data | Contact and point-of-contact fields dropped. Derived data scanned for email addresses and phone numbers | T8 | **Live, passing** |
| S9 | Disclaimer everywhere | Exact text held once in `src/disclaimer.py`. Appears in every page footer, at the top of the README, and in the header of every export | T6 | Stub |
| S10 | No legal conclusions | Nothing is described as compliant, non-compliant, lawful or unlawful. Findings describe what the data shows | T4 | Stub |
| S11 | Authorship | README and site footer credit the owner for the governance design. Nothing claims or describes who wrote the code | T6 for the credit line; a partial test for the second half, plus reading | **Live, passing** |
| S12 | Scope lock | Exactly three site views. No database, no login, no dashboard, no extra framework. Scope changes need owner approval in writing | T9 | Stub |

## Why raw data is not committed

Raw OMB files contain vendor and product columns. Committing them would break
S2. Instead the notebook downloads each file from its official URL and checks
its hash against `governance/data-provenance.md`. Anyone can reproduce the
results. The repository itself never holds a vendor name.

## Banned trend framing (owner addendum, 22 September 2026)

No count in this project is a safe trend. Inclusion criteria and consolidated
reporting changed between years, and the serious category was defined under a
different memorandum in each year. Comparing any two annual figures invites a
reading the data cannot support.

A list of trend verbs is therefore banned across the whole repository. The
authoritative list is held in two places only, and this file deliberately does
not repeat it so that it can stay subject to the ban itself:

- `governance/decision-rules.md` section 4, in the owner's words
- `tests/test_banned_words.py`, as the constant the test reads

Exempt from the check, as set by the owner: the test file itself, `CLAUDE.md`,
and `governance/decision-rules.md`. Everything else is in scope, including this
file.

Matching is on whole words, not substrings, so ordinary words that happen to
contain a banned one are not caught.

A word test cannot catch meaning. A sentence can imply a trend without using any
banned verb. **Phase 7 therefore includes a manual trend-framing review** of
every published sentence that mentions more than one year, recorded in the table
below.

### T2 exemptions (approved by the owner, 23 September 2026)

T2 scans every file, including markup, attributes and URLs. There is no
categorical exemption. Only these exact strings are exempt, and only where they
appear verbatim.

| Exact string | Reason it is exempt |
|---|---|
| `<meta charset` | Required HTML character-set declaration. One company shares the tag name. Not published copy |
| `<meta name="viewport"` | Required HTML declaration for mobile rendering. Same collision |
| `spheroidal elastic deformation sources` | A description of a physical property in a geophysics use case. One company shares the adjective. Verified as the only occurrence of that word in the derived data, with no variants, so the exemption is the full phrase rather than the word |

Vendor names can appear in `alt`, `title` and `aria-label` attributes and inside
link URLs. One was found inside a link during Phase 3. This is why the exemption
is two exact strings rather than a rule about markup.

**Adding any further exemption requires the owner's approval and is a
stop-and-ask condition.**

### The scope limit of S2 and T2

**Recorded by the owner on 23 September 2026 as a known and accepted limit, not
as work outstanding.**

T2 verifies that **no term on the blocklist survives** in published data or on
the site. It does **not** verify that no vendor name survives, and it cannot.

The blocklist is built from the field where an agency names its supplier. A
commercial product that an agency mentions only in narrative text, and never
enters in that field, is outside the blocklist and therefore outside the test.
Several such products have been found by hand and added individually, which
demonstrates that the category exists rather than that it has been emptied.

**Why this is accepted rather than closed.** Closing it would mean identifying
every commercial product name in free text written by 41 agencies across 3,611
entries. There is no field that lists them, so the only method is reading, and
each pass finds more. That is the same objection that refused the
exception-accumulation approach to the blocklist: **it has no natural stopping
point**, and an open-ended obligation presented as a control is worse than a
narrow control whose boundary is stated.

So the boundary is stated instead:

| Claim | Status |
|---|---|
| No term on the blocklist appears in published data or on the site | **Verified by T2** |
| No vendor name whatsoever appears in published data | **Not claimed, and not verifiable by this method** |

Anything published by this project describes the first claim, never the second.

### Scope of the trend-word ban: what counts as this project's prose

**Owner ruling, 24 September 2026.**

The ban exists to stop **this project** framing counts as a trend. Text written
by the agencies and published in the register is **data, not framing**. A use
case named after predicting a patient's loss of balance frames nothing.

The boundary is drawn **by key, never by file path.** This project's own prose
sits inside the same JSON files as the source values, and a trend sentence
written into a caveat is precisely what this test exists to catch. Excluding a
file wholesale would let that through.

**Any key not listed as source data is treated as project prose and is checked.
A new field therefore lands on the checked side by default.**

| Key | Treated as | What it holds |
|---|---|---|
| `rows` | **Source data** | One entry per register row: use case name, agency, stage, classification, identifier |
| `field` | **Source data** | A field name as one of the two registers publishes it |
| `oversight_field_coverage` | **Source data** | Keys are the register's own field names |
| `field_completeness_all_rows` | **Source data** | Keys are the register's own field names |
| `field_completeness_high_impact` | **Source data** | Keys are the register's own field names |
| `bands` | **Source data** | Keys are the classification labels in the data's own wording |
| `entries_flagged_at_highest_threshold` | **Source data** | Row positions, not text |
| Export file rows | **Source data** | Everything beneath the comment header of an export |
| `caveat`, `rule_applied`, `finding`, `question`, `statement`, `note`, `detail`, `name`, `label`, `never_summed_reason`, `why_reported_separately`, `dictionary_note`, `mechanism_differs_from`, `purpose`, `reason` | **Project prose** | Checked |
| Export file header | **Project prose** | Checked |
| Every `.html`, `.js`, `.py`, `.md` file not exempt | **Project prose** | Checked in full |

The scoping was verified in both directions before it was accepted: a trend word
planted inside a caveat is caught and reported with its exact key path, and
trend words planted inside a source use case name are not.

### A pattern worth naming: word tests meet text that is not prose

Four collisions have now occurred between a word list and text that nobody wrote
as prose. The fourth arrived within a day of this note being written, which is
the point of the note:

| Collision | What the match actually was | Resolution |
|---|---|---|
| A company name inside a required character-set declaration | Markup | Exact-string exemption |
| A banned word that was an HTML attribute on a control | Markup | **Fixed.** The control was rewritten to use a class, so no exemption was needed |
| Trend words inside agency-authored use case names | Source data | Scope statement, drawn by key |
| A banned word used as a variable name in site code | Code identifier | **Fixed.** The variable was renamed, so no exemption was needed |

A word test applied across a whole repository **will keep meeting text that is
not this project's writing.** That is a property of the method, not a series of
accidents, and it will happen again.

So the question each time is the same one: **is the match this project's own
writing?**

- **Yes**: it is a finding, and the copy is reworded. This has happened five
  times, once inside the paragraph explaining why the ban exists.
- **No**: it is either a fix that removes the collision outright, which is always
  preferable, or a scope statement recorded here.

What is never acceptable is the third option: taking the term off the list the
test reads. That makes the test pass while leaving the thing it was checking for
in place, and it has been attempted once in this project and reversed.

### S4 beyond vocabulary: who reads, and when

**Recorded 24 September 2026.**

T4 checks vocabulary. It cannot check framing. A sentence can imply movement
over time, or judgment of an organisation, without using a single listed word,
and no word list will ever reach that.

That gap is covered by **a human reading**, and this section names who does it
and when, because an untested gap with a named owner is a control and one
without is a hope.

| | |
|---|---|
| **Who performs it** | The developer, as a role. Not an individual, so it survives a change of hands |
| **What is read** | Every published sentence: the three pages, the README, the finding and caveat text in `findings.json`, and the export headers |
| **What is looked for** | Framing that implies a comparison between years, judgment of an organisation, or an inference about why a field is empty |
| **When it is repeated** | **Whenever published copy changes.** Not once at Phase 7. Any edit to a page, a caveat, a finding or the README triggers it again |
| **Where the result is recorded** | The Phase 7 manual-check table below |

The owner performs an independent reading of the same material. The two are not
substitutes: the developer's reading is part of shipping a change, the owner's
is acceptance.

### Claims against evidence: the second reading, same owner

**Recorded 29 September 2026**, after a heading was found claiming the opposite
of the finding directly beneath it.

The suite verifies **wording, structure and provenance**. It does not verify
that a claim matches the evidence under it, and no test can: that means holding
both in mind and asking whether they agree.

| | |
|---|---|
| **Who performs it** | The developer, as a role. The same owner as the neutral-language reading |
| **What is read** | Every heading, lead-in and summary sentence on the three pages, against the figure or finding it sits above |
| **The question asked of each** | Does this claim more than the thing beneath it supports, or something different from it |
| **When it is repeated** | **Whenever published copy changes**, alongside the neutral-language reading |
| **Where the result is recorded** | The Phase 7 manual-check table below |

**What it caught on its first pass:** one heading claiming the opposite of its
finding, one making a causal claim the data supports only as association, one
describing entries as sorted when several hundred were not sorted at all, and
one stating an absolute where two entries out of hundreds sit in between.

The owner performs an independent reading. As with neutral language, the two are
not substitutes.

### The second half of S11

S11 also requires that nothing claims or describes who wrote the code. That is
an absence, and an absence cannot be proved by searching.

`tests/test_authorship_claims.py` looks for the phrasings such a claim would
most likely take. It **catches likely forms only and does not prove the
absence**, and it says so in its own docstring so that nobody reads a green tick
as more than it is. The reading described above covers the rest.

It earned its place immediately: it caught an ambiguous phrase in a source
comment describing what produces the site's data. The phrase was reworded.

### Where each rule lives: the single-source audit

**Carried out 28 September 2026**, after a rule implemented twice was found to
have drifted. Full account in the README process notes.

| Rule | Single source | Status |
|---|---|---|
| What counts as an empty value | `data/raw/empty_value_rule.json` | **Was duplicated in page code and had drifted, 28 values against 21. Now published by `scripts/build_data.py` and fetched by the page.** A test fails if any script sets the list out again |
| Which fields count towards completeness | `src.measures.CORE_FIELDS` | **Was duplicated in an ad-hoc generator. Now imported by `scripts/build_data.py`**, which is the only thing that writes the table |
| The disclaimer, export notice, authorship, Ontario attribution | `src/disclaimer.py` | Single source. T6 compares every published copy against it |
| The vendor blocklist | `data/raw/vendor_terms.txt` | Single source. The scrub and T2 read the same file |
| The term matcher | `src.scrub.compile_term_pattern` | Single source. The scrub and T2 import the same function, so the test cannot be weaker than the fix |
| Similarity thresholds | `src.measures.SIMILARITY_THRESHOLDS` | Single source |

### Two duplications that remain, by design

These are recorded rather than removed, because both exist to be read by a
person and the executable copy is not readable as a rule.

| Rule | Copies | Why it stays |
|---|---|---|
| The banned trend verbs | `tests/test_banned_words.py` and `governance/decision-rules.md` | The decision document records the owner's rule in the owner's words. The test file holds the list the check reads. `safeguards.md` deliberately restates neither and points at both |
| The T2 exact-string exemptions | `tests/test_no_vendor_terms.py` and `governance/safeguards.md` | The test holds what is exempt. The safeguards document holds why, which is the part a reviewer needs |

**The risk is real and is accepted with its mitigation named.** Both pairs can
drift the way the emptiness rule did. What prevents it is that adding an
exemption is a stop-and-ask, so neither copy changes without the owner, and the
owner sees both. If that ever stops being true, these become single-source too.

### Phase 7 manual checks

| Check | Why a test cannot do it | Reviewed on | Outcome |
|---|---|---|---|
| Trend framing review. Every published sentence mentioning more than one year is read for implied comparison | Implication is carried by sentence structure, not vocabulary | not yet run | |
| S1 source attribution complete and accurate | Requires reading the sources | not yet run | |
| S11 authorship, and no claim about who wrote the code | Requires reading for absence | not yet run | |

## Scope changes

Any change to the scope recorded under S12 is written here, dated, and signed
off by the owner before work starts.

| Date | Change requested | Owner decision |
|---|---|---|
| 2026-09-24 | Scope the trend-word ban to this project's own prose, excluding values copied unchanged from the source register | **Approved.** The ban exists to stop this project framing counts as a trend. Agency-authored text in the register is data rather than framing, and the only ways to satisfy the rule literally were to alter the source data or to stop publishing the register. Implemented by key rather than by file path, so that project prose inside a data file stays checked, and recorded above so the boundary is auditable |
