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
| The landing page's evidence figures | `data/derived/findings.json` and `reusability_findings.json` | Single source. **Resolved when the site is built rather than in the browser, from 30 September 2026.** `tests/test_evidence_figures.py` re-reads the findings and fails if a published figure has drifted from the one it came from |

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

### Where the landing page's figures are resolved, and why that changed

**Changed 30 September 2026.** The landing page used to fetch every finding on
the site, in two files, to read five numbers out of them in the browser. It now
reads figures that the build has already resolved into `fieldset.json`.

| | Before | After |
|---|---|---|
| Where the figure is read from the finding | In the reader's browser, on every visit | Once, when the site is built |
| Files the landing page downloads | 6 | 4 |
| Bytes | 72,386 | 61,855 |

**What this gives up, and what replaces it.** Reading the finding in the browser
meant a figure could not be stale, because it was resolved from the finding
every time the page loaded. Resolving at build time means a published figure
could in principle sit still while the finding it came from moves.
`tests/test_evidence_figures.py` closes that: it re-reads both findings files
and fails, naming the path, if any published figure or denominator disagrees.
It was verified by planting the failure, moving one resolved value by one.

S5 is unaffected either way. Every number is still computed from the data by a
script and published from `data/derived`. What changed is when the lookup runs,
not whether the number is traceable.

A second test asserts that `proposal.js` does not fetch the findings files
again, because the saving only holds while the page stops asking for them.

### The two exact-string exemptions for the repository address

**Approved by the owner on 30 September 2026.** Publishing a link to the
project's own source would otherwise fail two tests. Each exemption covers one
exact string and nothing else.

| Test | What it would otherwise catch | Why the exemption | Scope |
|---|---|---|---|
| T2, no vendor or product terms | The hosting provider's name sits inside the address | A reader cannot check the working without being told where it is. The provider's name is unavoidable in its own URL and names no vendor of an AI system | The exact value of `src.disclaimer.REPOSITORY_URL`, nowhere else |
| T5, no typed numbers in published pages | Digits inside the account name | The digits are part of an address, not a figure a reader could mistake for a finding. Every other number on the page stays checked, including any printed beside the link | The exact value of `src.disclaimer.REPOSITORY_URL`, nowhere else |

**Neither is a categorical exemption.** Both read the one address from
`src.disclaimer.REPOSITORY_URL` rather than holding a pattern, so widening
either means changing that value, which is a stop-and-ask. While the value is
empty, nothing is exempt and no link is rendered.

**Verified by planting the failure.** With the address set, both tests pass and
the link renders. With a second, different address added to the same page, T2
reports `docs/index.html: ['github']` and T5 reports `index.html:122 '9999'`.
The exemptions cover the approved address alone.

**Live since 29 September 2026.** The owner created the repository and sent the
address, so `REPOSITORY_URL` now holds it and the link renders on the landing
page and in the README. The full suite was run with the address set: 48 tests
pass, which is what confirms both exemptions are drawn narrowly enough to let
the approved address through and nothing else.

### What colour means on the landing page

**Set 30 September 2026.** Colour on the landing page carries meaning, so it is
rationed. Two hues, and nothing else.

| Token | Means | Used by |
|---|---|---|
| `--pub` | The published register: the file this project read, and anything leading back to a finding about it | The slot marks, the left form's heading and box edges, every link on the page, the evidence figures |
| `--mine` | The field set: the author's own proposal, which is what this page argues for | The opening figures, the right form's heading and box edges, the field card numbers, the open card's edge |

Everything else on the page is neutral. Links take `--pub` rather than a third
colour, because every link on this page leads to the audit of the published
register.

**Nothing else may borrow either hue.** If a third thing needs telling apart, it
is told apart by shape, weight or position. The rules that carry these meanings
are scoped to `main.design-page`, so they cannot reach the three audit pages.
The tokens they replaced, `--real`, `--fiction` and the `--side-*` set, were
deleted rather than left unused, because an unused hue in the stylesheet is what
lets something borrow it later.

**Nothing depends on colour alone.** The three states a box can be in are told
apart by shape and by words: a filled box has a solid edge, a ground and its
content; a box the register does not collect has a dashed edge, no ground and no
content; a box the register asks and the entry leaves empty has a solid edge and
no content. Each empty box carries a caption underneath saying which it is. The
slot strip pairs solid and hollow marks with a caption stating the same split in
words.

## Scope changes

Any change to the scope recorded under S12 is written here, dated, and signed
off by the owner before work starts.

| Date | Change requested | Owner decision |
|---|---|---|
| 2026-09-29 | Add a fourth page: the author's design view | **Approved.** The brief set three views describing the register. A fourth states what the author would build from what the audit found, which is a different kind of claim and is kept on a page of its own. Every field on it traces to a finding, it states its own limits, and nothing on the three findings pages changed to support it |
| 2026-09-30 | Merge the planned fifth page, a dashboard, into the fourth, and make that the landing page | **Approved.** The dashboard was to carry framing, a preview of the field set, and the key figures. All three already belonged on the design page, and a separate page would have restated them. Merging keeps the site at four pages rather than five, and puts the design view and the evidence it rests on in one place. The register moves to its own tab. Figures on the evidence strip pass the caveat test or are linked rather than reproduced |
| 2026-09-30 | Draw the form, add the slot strip, set three levels of hierarchy, and cut colour back to two meanings | **Approved.** The page was text at one weight in identically treated cards, with no shape anywhere, so a first-time reader had to build a mental model of a register entry by reading. The two worked examples become two drawn copies of the same form, label above box, with the published entry's unanswerable boxes left visibly empty. Ten marks beside the opening state the split at a glance. Three levels: the opening and the forms loud, the evidence and field set secondary, sources and where-to-go-next quiet. Contrast is carried by density rather than shade, and every figure stays computed from the data |
| 2026-09-30 | Replace the counting numeral with the slot fill | **Changed during the work, and reported.** The instruction was for the headline figure to count up. Counting from zero printed figures that were not the finding: mid-count the sentence read "of 1 things ... answers 0", which contradicted the slot strip beside it. The slots now fill one at a time instead. It counts the same thing, reveals the same fact, and can only ever show the real split |
| 2026-09-30 | Restructure the landing page: worked panels first, field set into closed cards, and motion that reveals | **Approved, with constraints set by the owner.** The order becomes headline, the two worked panels, the evidence strip, then the field set and the way on to the register. The ten fields close by default; the owner recorded that their earlier ruling to open everything applied to the five sections on the gaps page, not to these. Motion is allowed only where it makes a fact easier to see, must honour `prefers-reduced-motion` in full, must leave every section reachable without triggering anything, must degrade to one column and stay reachable by keyboard, and must not make the page heavier or slower |
| 2026-09-24 | Scope the trend-word ban to this project's own prose, excluding values copied unchanged from the source register | **Approved.** The ban exists to stop this project framing counts as a trend. Agency-authored text in the register is data rather than framing, and the only ways to satisfy the rule literally were to alter the source data or to stop publishing the register. Implemented by key rather than by file path, so that project prose inside a data file stays checked, and recorded above so the boundary is auditable |
