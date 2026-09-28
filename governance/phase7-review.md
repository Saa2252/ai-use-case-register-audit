# Phase 7. Safeguard review

Twelve safeguards, the test that enforces each, and what that test does not
cover. Then the four documented scope statements, then the checks no test can
perform.

**Suite status: 23 tests, all passing.**

A test that passes proves one narrow thing. The column that matters most below
is the third.

---

## S1. Source attribution

**Enforced by:** T1 row counts and T7 file hashes, plus `data-provenance.md`,
which records every URL, download date, SHA-256 hash, licence and field mapping.

**What the tests prove:** the files analysed are byte-for-byte the files
downloaded, and they still hold the row counts recorded at download.

**What they do not cover:** whether the attribution is *correct*. No test can
confirm that a URL is the official source rather than a mirror, that the licence
named is the licence that applies, or that the Ontario attribution wording
matches what the licence demands. That wording was copied verbatim from the
licence page and the clause requiring it is quoted in provenance, but a human has
to agree it is right.

---

## S2. No vendor or product names

**Enforced by:** T2, which checks that no term on the blocklist appears anywhere
in `data/derived/` or `docs/`, matched case-insensitively and tolerant of
spacing and punctuation. The scrub and the test import the same matcher, so the
test cannot be weaker than the fix.

**What the test proves:** no listed term survives in anything published.

**What it does not cover:** that no vendor name survives. The blocklist is built
from the field where an agency names its supplier. A commercial product an
agency mentions only in narrative text never reaches that field and is outside
the list. Several were found by reading and added by hand, which shows the
category is real rather than that it has been emptied. Recorded as an accepted
limit, not outstanding work. See scope statement 3.

---

## S3. No agency judgments

**Enforced by:** T3, in two parts. No ranking or comparison language on any
page, and no finding in `findings.json` names an individual agency.

**What the tests prove:** the site carries no league table, score, rank or
cross-agency comparison, and no published finding is broken down by agency.

**What they do not cover:** a comparison made without any of the words the test
looks for. Two figures placed side by side, or an ordering that implies one, can
invite a comparison the copy never states. This needs reading. See manual check
2.

---

## S4. Neutral language

**Enforced by:** T4, in three parts. The banned word list from the brief, across
pages, README, findings and exports. The trend-verb ban across this project's own
prose wherever it appears. And a check that the crosswalk caveat is absent,
because publishing it would imply an analysis this project does not perform.

**What the tests prove:** no banned word appears in published copy, and no trend
verb appears in anything this project wrote.

**What they do not cover:** framing. A sentence can imply movement over time, or
judgment of an organisation, without using a single listed word. This is the
largest gap in the suite and the reason manual check 1 exists.

---

## S5. Traceable numbers

**Enforced by:** T5, plus three supporting tests. T5 confirms no number of three
or more digits is written into any page outside the disclaimer and dates. The
supporting tests confirm every `data-figure` path resolves inside the published
JSON, that every page loads the script that fills them, that every data file the
scripts request exists, and that a page whose data does not load says so rather
than showing figures as unavailable.

**What the tests prove:** every figure on the site is loaded from
`data/derived/`, asks for something that exists, and announces its own failure.

**What they do not cover:** whether the figure is *right*. The tests confirm the
number came from the notebook. They cannot confirm the notebook computed the
right thing. That is what the caveats and the provenance record are for.

---

## S6. Reconcile to published totals

**Enforced by:** T1, which checks row counts against the totals recorded in
provenance.

**What the test proves:** the files still hold the counts they held at download,
so a silent change would stop the suite.

**What it does not cover:** the three published figures that do not reconcile.
The test guards the four that do. The three that disagree are published as
findings with both candidate explanations stated and neither chosen, which is a
judgment no test makes.

---

## S7. Raw data untouched

**Enforced by:** T7, which re-hashes every raw file against the manifest written
at download.

**What the test proves:** no raw file has been edited since it arrived.

**What it does not cover:** anything, if the raw files are absent. The test
skips rather than passes when the manifest is missing, so a clone without the
downloads reports a skip and not a green tick.

---

## S8. No personal data

**Enforced by:** T8, which scans `data/derived/` and `docs/` for email addresses
and telephone patterns.

**What the test proves:** no address or telephone pattern is published, and it
now scans the field-level file the row detail downloads.

**What it does not cover:** a person named in free text without an address
beside them. A name alone matches no pattern. The contact field was removed
whole, and one address inside a description was scrubbed, but a personal name
written into a narrative field would survive.

---

## S9. Disclaimer everywhere

**Enforced by:** T6, in four parts: the exact disclaimer on every page and in the
README, the authorship line on every page, and both the disclaimer and the
practice-exercise notice in every export header.

**What the tests prove:** the required text is present and identical to the
single constant it is generated from, so it cannot drift between files.

**What they do not cover:** whether a reader sees it. Presence in the markup is
not prominence on the page.

---

## S10. No legal conclusions

**Enforced by:** T4, whose word list carries the legal terms from the brief.

**What the test proves:** nothing published describes anything as compliant,
non-compliant, lawful or unlawful.

**What it does not cover:** a legal conclusion drawn without legal vocabulary.
Saying a register does not hold what an oversight body would need is close to
such a claim, and the caveats exist to hold that line. Needs reading.

---

## S11. Authorship

**Enforced by:** T6 checks the authorship line is on every page. The README
carries it too.

**What the test proves:** the owner is credited for the governance design,
identically, everywhere.

**What it does not cover:** the second half of the safeguard, which is that
nothing claims or describes who wrote the code. Absence cannot be tested for
without a list of every way it could be said. See manual check 4.

---

## S12. Scope lock

**Enforced by:** T9, in three parts: exactly three HTML pages, no database
files, and no login code anywhere on the site.

**What the tests prove:** the site is still three static pages with no account
system and no database.

**What they do not cover:** scope expanding within a page. The three views have
gained a register table, filters, row detail and cross-view links, all within
the brief, but nothing counts pages' worth of content. Whether the project still
does what it said it would is a reading, not a count.

---

# The four documented scope statements

## 1. T2 exact-string exemptions

Three exact strings are exempt from the vendor-term check: two required HTML
declarations whose tag name a company shares, and one description of a physical
property in a geophysics entry whose adjective a company shares. Verified as the
only occurrence of that word, with no variants.

**Not a categorical exemption.** Vendor names appear in link URLs and can appear
in image and label attributes, and one was found inside a link during Phase 3.
Adding a fourth exemption requires the owner and is a stop-and-ask.

## 2. T4 key-based scoping

The trend-verb ban applies to this project's own prose, wherever it appears,
including prose inside data files. Values copied unchanged from the source
register are excluded.

**Drawn by key, never by file**, because project prose and source values sit in
the same files. A trend sentence written into a caveat is what the test exists to
catch. Any key not listed as source data is checked, so a new field is checked by
default. Verified in both directions before acceptance.

## 3. The S2 vendor-field limit

T2 verifies that no blocklist term survives. It cannot verify that no vendor
name survives, because the list is built from the vendor field and commercial
names appearing only in narrative text are outside it.

**Accepted rather than closed.** Closing it would mean reading every free-text
field across 41 agencies and 3,611 entries with no way to know when the work was
complete. Later findings go to `known_issues.json`.

## 4. The held-back terms

Six commercial names that are also ordinary English words are held off the
blocklist, because a case-insensitive rule on them would replace ordinary prose.
Each was checked in context: four appear in the register and none carries a
commercial meaning there, two do not appear at all.

Published with the reason for each and the instruction to re-check every one if
the source is downloaded again.

---

# Manual checks: for the owner to perform

No test performs these. Each needs someone to read.

## 1. Trend framing by implication

Read every published sentence that mentions more than one year, or places two
counts near each other. The word test catches vocabulary. It cannot catch a
sentence that implies movement without using a listed word.

**Where to look:** View 2's reconciliation section, the M1 consolidated-route
paragraph, and anywhere the earlier inventory is mentioned.

## 2. Sentences readable as a claim about an agency's conduct

Read the headline and every finding as though you were the agency named in the
row beneath it. The rule is that findings describe the data, never the conduct
of an organisation.

**Where to look:** the View 1 headline, the oversight block on View 3, the
clustering observations, and any sentence with an agency as its subject.

## 3. Remaining inference in either direction

The clause cut from View 3 explained why a field was empty. Look for any other
sentence that explains an absence rather than reporting it.

**Where to look:** the classification-not-recorded band, the presumed band, the
oversight block, and the completeness-shape finding.

## 4. No claim about who wrote the code

S11 credits the owner for the governance design and requires that nothing claims
or describes who wrote the code. Read the README and the pages for any sentence
that does.

## 5. Wording preference on field sets

Prefer "not present in the 2025 field set" over words that attribute an act to
someone, when comparing what each year asks.

**Where to look:** View 2's trigger groups and the M5 comparison.

## 6. Source attribution accuracy

Confirm the sources named are the official ones, the licences are right, and the
Ontario attribution matches what the licence demands.
