# Learning log

One entry per phase. What we did, why it matters in real AI governance work,
new terms, decisions made, and one interview question with a model answer.

---

## Phase 0. Setup

**What we did**

Created the empty skeleton of the project before touching any data: folders,
a `.gitignore` that blocks raw data from ever being committed, pinned software
versions, three governance documents as stubs, three empty site pages, and ten
test files, one for each safeguard.

Nothing was downloaded. Nothing was analysed. That is the point.

**Why it matters in real AI governance work**

In a real organisation the order of operations is the credential. Anyone can
produce a chart. Far fewer people can show that the rules, the evidence trail
and the tests existed *before* they saw the data, because that is what makes the
result hard to argue with later.

Three specific habits were set up here:

- **The evidence trail came first.** `governance/data-provenance.md` exists and
  is empty, waiting for URLs, dates and hashes. An auditor's first question is
  never "what did you find", it is "where did this come from".
- **The safeguards are executable.** Each of the twelve rules has a test file.
  A rule that lives only in a policy document is an intention. A rule with a
  test that stops the build is a control.
- **The decisions are reserved for the owner.** `governance/decision-rules.md`
  is deliberately blank. The counts this project reports will depend entirely on
  rules that have not been set yet, and setting them is a governance act, not a
  technical one.

**New terms**

- **Register** or **use case inventory**: the list an organisation keeps of the
  AI systems it uses. The starting point of almost all governance work.
- **Provenance**: the record of where a file came from, when it was obtained,
  and proof it has not changed since.
- **Hash** (SHA-256 here): a fingerprint of a file's contents. Change one
  character and the fingerprint changes. It is how you prove a file was not
  edited.
- **Reproducibility**: someone else can re-run the work and get the same
  numbers without asking you for anything.
- **Derived data**: any file the analysis produces from the raw source.
  Everything published comes from derived data, never from raw.
- **Scope lock**: a written limit on what the project will contain, so that
  additions have to be argued for rather than drifting in.

**Decisions the owner made**

| Decision | Reasoning |
|---|---|
| Authorship line reads "Governance design by Sana Ahmad." | Required by safeguard S11 |
| Repository lives in a new empty folder, `/Users/tigersaa/__CODE/AI Usecase inventory` | Keeps the project self-contained and outside any existing repository, which matters for GitHub Pages in Phase 9 |

**Interview question you could be asked**

*"You audited a published AI use case inventory. Where did you start?"*

Model answer: "Before looking at the data I wrote down three things: where every
file came from and how I would prove it had not changed, the rules the published
output would have to obey, and an automated test for each of those rules. I also
left the analytical decisions blank on purpose, because questions like 'what
counts as one use case' change every number in the report and they are
governance decisions, not technical ones. Doing that first meant that when the
numbers came out, the only thing left to argue about was the data."

---

## Between Phase 0 and Phase 1: owner addenda and environment

**What we did**

Three source URLs were checked before any environment work, because a moved
source would have changed the plan. All three are live. The 2025 inventory still
states the totals recorded in the brief, so the reconciliation baseline holds.

The owner then issued a set of rulings on how the two years may be compared, and
Python 3.11 was installed with the pinned packages.

**Why it matters in real AI governance work**

The owner's rulings are the most valuable thing in the repository so far, and
none of them came from the data.

The central one is **definition drift**. The serious category was rewritten
between the two years under different OMB memoranda, so the two counts do not
measure the same population. The obvious chart, one bar per year, would have
been wrong in a way that no amount of careful wording could fix. The owner
banned it outright and then widened the ban, on the reasoning that no count in
this project is a safe comparison between years, because inclusion criteria and
consolidated reporting also changed.

Two habits are worth noticing in how that was handled:

- **The rule was made executable and its limits were named.** A banned word list
  went into the test suite, and because a word test cannot catch implication, a
  manual review was booked into Phase 7 to cover what the test cannot see. A
  control that knows its own blind spot is worth more than one that does not.
- **The control was tested against the project's own writing immediately.** It
  caught three sentences written for this repository, including one that used a
  banned word to describe not doing the banned thing. Rules that are only
  applied to other people's work are not rules.

**New terms**

- **Definition drift**: the rule for counting something changes between periods,
  so the number moves for reasons that have nothing to do with the world.
- **Crosswalk**: a comparison at the level of individual entries rather than
  totals. Says what happened to specific items, not to a population.
- **Consolidated off-the-shelf reporting**: one register line standing for many
  commercial systems. New in 2025, and the reason a missing 2024 entry may have
  been folded in rather than dropped.
- **Virtual environment**: a private copy of Python belonging to one project, so
  that re-running the analysis gives the same answer on a different machine.

**Decisions the owner made**

| Decision | Reasoning |
|---|---|
| The two years' category counts are never a trend, and never share a sentence, table row or chart | Different memoranda, different populations |
| Carry-forward still runs, but a 2024 entry is checked against the 2025 consolidated file before being called not carried forward, and the match count is published | Consolidated reporting is new, so the unchecked figure would overstate |
| Trend verbs banned across the whole repository, three files exempt, plus a manual review at Phase 7 | No count here is a safe comparison, and a word test cannot catch meaning |
| The three-state category stays a Phase 4 decision, with Phase 2 reporting the numbers first | The decision needs the evidence underneath it |
| Headline pool excludes pairs built on either the category counts or the totals | The disagreement would be an artefact of the rules, not a finding |

**Interview question you could be asked**

*"You had two years of the same government inventory. Why not show the change?"*

Model answer: "Because the definition changed underneath the number. The two
years applied different memoranda, the serious category was rewritten rather
than renamed, and a new consolidated reporting route appeared in the second
year. So a bar chart with one bar per year would have been measuring the rule,
not the world. What I could honestly do was compare individual entries that
appear in both years, with a caveat saying the data cannot tell you whether a
reclassification reflects the new definition or an agency's own reassessment.
The first thing I check when comparing registers over time is whether the
definitions held still, and here they did not."

---

## Phase 1. Acquire and verify

**What we did**

Downloaded twelve files by script from three sources, hashed every one, archived
the source pages, and checked every figure the publisher states against the
files themselves. Wrote nothing to `data/derived/`. No field was dropped, no
value was changed.

Four of the seven published figures reconcile exactly. Three do not. Under
safeguard S6 the work stopped there and went back to the owner.

**Why it matters in real AI governance work**

This is the phase that decides whether anything downstream can be trusted, and
it is the phase most projects skip.

Four things are worth drawing out:

- **Reconciliation is the whole point of the phase.** A row count that matches
  the publisher's stated total is the cheapest possible evidence that you are
  analysing what you think you are analysing. Where it did not match, the
  mismatch became a finding rather than a problem to smooth over.
- **The source disagrees with itself.** Summing the per-agency table in the
  publisher's own README gives a different answer from the TOTALS row printed
  underneath it, by one. Nobody would have found that without adding up a table
  that already had a total on it. Checking the arithmetic you were handed is
  not pedantry, it is the job.
- **The crosswalk could not run, and that is a result.** The earlier year's file
  has no identifier column of any kind, so entries cannot be matched between
  years by identifier. Reporting that honestly is worth more than quietly
  switching to matching on names and presenting the output as though it were the
  same thing.
- **A rule fired and stopped the work.** The stop-and-ask conditions were written
  before the data arrived, and they triggered on their own terms. A control that
  has never stopped anything has not yet been tested.

**New terms**

- **Reconciliation**: checking that the data you hold matches the totals the
  publisher says it contains, before doing anything else with it.
- **SHA-256 hash**: the fingerprint written down at download, so the file can
  later be proved unchanged.
- **Character encoding**: the scheme mapping bytes to letters. One of the source
  files is cp1252, not UTF-8. Read with the wrong scheme it appears corrupt
  rather than merely different, which is an easy way to conclude a file is
  damaged when it is fine.
- **Normalisation**: making values comparable before matching them. One agency
  name appears twice in one file, differing only by a trailing space.

**Decisions the owner made**

| Decision | Reasoning |
|---|---|
| Reconcile against all seven stated figures, not two | A partial check is not a check |
| Sum the publisher's own per-agency table against its printed total | Internal inconsistency in a source is itself a finding |
| Archive both source pages | The repository updates on a rolling basis and one agency's inventory is still forthcoming |
| Paraphrase the source, never quote it, where its wording contains a banned word | Avoids needing an exemption in the test |

**Decisions now waiting on the owner**

Three figures that do not reconcile, the absence of cross-year identifiers, and
whether the register design comparison still holds against a source with three
rows.

**Interview question you could be asked**

*"What did you do when the data did not match the published total?"*

Model answer: "I stopped and reported it, because I had written down before
starting that I was not allowed to adjust the expected number myself. Three of
seven published figures did not reconcile. One gap turned out to be exactly the
number of rows with a blank stage field, which is consistent with two different
explanations that the data cannot separate, so I wrote down both rather than
picking one. I also added up the publisher's own per-agency table and found it
disagreed with its own printed total by one. None of that means anything is
wrong at the publisher. It means the numbers need stating carefully, and that
the person reading my analysis should know which figures are solid and which
are not."

---

## Phase 2. Profile

**What we did**

Read both data dictionaries, mapped every field used to its definition, profiled
the completeness of all 36 columns of the 2025 file, compared the field sets
across the two years, and identified the contact and vendor fields for removal
in Phase 3. Nothing was removed yet.

**Why it matters in real AI governance work**

Profiling is where you find out whether the register can answer the questions
people will ask of it. Four things came out of it.

- **An empty answer is not always blank.** Two fields store "nothing selected"
  as the literal text `[]`. Counted naively, both read as 100% complete. Read
  correctly, one is 30.6% and the other 7.3%. The error runs about seventy
  percentage points in the direction that flatters the register. Anyone
  profiling a register needs to look at what an empty answer actually looks like
  in that file before counting anything.
- **Blocks of fields behave as blocks.** Within the entries flagged high-impact,
  nine oversight fields are answered together or not at all: 126 rows answer all
  nine, 317 answer none, and only 2 are partial. That is a fact about how
  submissions arrive, and it means "average completeness" would have described
  nothing real.
- **A conditional question is a form instruction, not a data rule.** Three
  fields are specified to appear only under stated conditions, and all three
  carry values in rows that do not meet them. The specification describes what
  the form shows, not what the file may contain.
- **What a register stops asking is a finding.** 2024 asked whether the AI can
  act without direct human involvement. 2025 does not ask it. Nothing in the
  data announces that. It is only visible by comparing the two field lists.

**New terms**

- **Data dictionary**: the document defining each field, its allowed values and
  when it applies. The thing you read before the data, not after.
- **Conditional field**: one the form shows only when an earlier answer takes a
  particular value.
- **Completeness**: the share of rows where a field holds a real value. Only
  meaningful once you know how that file writes an empty answer.
- **Character encoding**: the scheme mapping bytes to characters. Published with
  the wrong assumption, a file appears damaged rather than merely different.

**Decisions the owner made**

| Decision | Reasoning |
|---|---|
| The withheld overlap figure stays withheld, reason recorded, and the escalation itself is described in the README | A caveat does not survive being quoted, and discarding it would have hidden the judgment |
| The conditional-field mismatch becomes a primary finding, framed as data against dictionary, clustering as observation only | It is the clearest structural thing in the file, and the framing keeps it about data |
| The 1.3% figure never appears without its dictionary explanation in the same paragraph | Separated, the number says the opposite of what is true |
| Headline candidate on identifiers ranked first | Identifier absence has consequences for every future year |
| Encoding published as a reusability finding | A register published for reuse has to open |

**Interview question you could be asked**

*"You profiled a public register. What did you find that a spreadsheet would not
have shown you?"*

Model answer: "Three things. First, two fields recorded an empty answer as a
literal empty list rather than a blank, so a straight completeness count
reported them as fully populated when one was actually under a tenth filled.
Second, a block of nine oversight fields turned out to be answered all together
or not at all, which tells you something about how submissions are produced that
an average across the nine would have hidden completely. Third, comparing the
two years' field lists showed the register had stopped asking whether the system
can act without human involvement. None of those are visible by looking at the
data. They come from reading the dictionary alongside the file and then checking
whether the file behaves the way the dictionary says."

---

## Phase 3. Scrub

**What we did**

Built a vendor term list from the 2025 files, dropped four columns carrying
vendor, product or contact information, replaced vendor mentions in twelve text
fields with `[product]`, and wrote the scrubbed register to `data/derived/`.
Implemented the two tests this phase is judged by. T8 passes. T2 does not.

**Why it matters in real AI governance work**

Redaction is where good intentions meet a text file, and it went wrong twice
before it went right.

- **A blocklist built from free text is mostly not a blocklist.** The vendor
  column contains vendor names, but it also contains ordinary descriptions,
  agency names and filler answers. Taking every value as a term produced 4,662
  replacements, roughly two thirds of them ordinary words. A register with the
  words for decisions and searching replaced by `[product]` would have looked
  thoroughly redacted while removing almost nothing that mattered.
- **Over-redaction is not the safe direction.** It is tempting to think that
  scrubbing too much is the cautious error. It is not. It destroys the meaning
  of the text, and it creates a false impression of how much sensitive content
  the register held.
- **The most important thing that happened this phase was a test failing.**
  T2 failed because two real company names collided with web markup. The quick
  fix was to take them off the list. That made the test pass, and it left both
  companies named in the published register, one of them in a link. Removing a
  term from the list the test reads is not fixing the problem. It is editing the
  evidence. The terms went back on and the collision was escalated instead.
- **A false positive and a failure are not the same thing.** What remains is
  markup, not published copy. Saying so is not the same as making it go away,
  and the difference is the owner's to rule on, not the analyst's.

**New terms**

- **Blocklist**: the list of terms to remove. Here it is itself sensitive, so it
  lives outside the committed repository.
- **False positive**: a match that is not the thing being looked for. A test
  with many of them gets ignored, which is its own risk.
- **Over-redaction**: removing more than necessary, damaging meaning and
  overstating how much was sensitive.

**Decisions the owner made**

| Decision | Reasoning |
|---|---|
| 2024 reclassified as a schema reference, no row-level use anywhere | A structural limit cannot be forgotten by a later phase the way a caveat can |
| The overlap figure is permanently out of scope, not withheld | The analysis that produced it is now forbidden |
| Encoding and the two-file contradiction stay as reusability findings | Neither makes a claim about any entry |

**Interview question you could be asked**

*"Tell me about a time a control you built got in your way."*

Model answer: "I had a test that failed because two company names appeared in
the published output. They turned out to be inside HTML markup rather than in
anything a reader sees, and the fastest fix was to drop those two names from the
list the test checks against. I did that, the test passed, and then I looked at
the output and found both companies still named in the data itself, one of them
in a link. I had edited the evidence rather than fixed the problem. I put the
terms back, cleaned the data properly, and escalated the part that was genuinely
a false positive, because narrowing what a control examines is a decision for
whoever owns the control, not for the person the control is inconveniencing."

### Phase 3 addendum: final figures after the owner's rulings

The scrub was re-run three times under successively better rules. The
replacement count went 4,662, then 1,637, then 1,540, then 1,339. Every
reduction removed matches that were never vendor names.

The placeholder scan changed six published figures, including the headline
candidate: rows with no usable identifier moved from 704 to 706, because two
rows carry "TBD" in the identifier field rather than leaving it blank.

One distinction was worth the whole scan. A value only records an absence in a
field that expects written content. In a multiple-choice field the same words
can be a valid selection, and the dictionary lists "Not applicable" as an
allowed answer to two of the oversight questions. Treating it as empty
everywhere would have broken the oversight-block finding on a mistake.

**Term to add:** a **controlled vocabulary** is a fixed list of allowed answers.
Text that looks like an absence inside one is usually an answer.


## Phase 4. Decision rules

**What we did.** Wrote down the rules that decide the numbers, before running
the analysis that produces them. What counts as one use case. What counts as
empty. Whether the two years may be compared. Which words are banned from the
findings.

**Why it matters.** Most of what determines a figure in governance work is not
technical. It is a definition someone chose. Choosing after seeing the results
means choosing the result. Writing the rule down first, in the owner's words,
is what makes the figure a finding rather than a preference.

**New terms.**
- **Decision rule.** A definition fixed in advance and applied without
  exception, recorded with what it catches and what it misses.
- **Controlled vocabulary.** A fixed list of allowed answers. Text that looks
  like an absence inside one is usually an answer, not a blank.

**Decisions the owner made, and why.** One row is one use case, with lookalikes
flagged and never merged, because merging changes a published total on a
judgment that cannot be defended entry by entry. All three similarity
thresholds are published together, because publishing one would leave a reader
unaware that the number is a choice. No count anywhere is framed as movement over time.

**Interview question.** *How do you stop an analysis from being shaped by what
you want it to show?*
Fix the definitions before you look. Write down what each one catches and what
it misses, and publish the alternatives you rejected alongside the number. If a
figure depends on a threshold, publish every threshold rather than the one that
reads best.

## Phase 5. Analysis

**What we did.** Implemented the five measures, wrote every output to
`data/derived/` as JSON, and attached a caveat to every finding. Two of the
five turned into findings about what the register cannot answer rather than
measurements of it.

**Why it matters.** A measure that the data cannot support is itself a result.
Reporting "the register records no date on which an entry was checked" is more
useful to an oversight team than a freshness score built on a date field that
answers a different question.

**New terms.**
- **Derived data.** Outputs computed from raw files and never edited by hand.
  Everything published reads from here.
- **Caveat field.** A qualification stored with the figure, so the two cannot
  be separated by anyone republishing it.

**Decisions the owner made, and why.** Freshness became a finding rather than a
metric, because the data cannot support the metric. The two years are never
compared at row level: the earlier file carries no identifier for any entry, the
central category was redefined between them, and the inclusion rules changed.

**Interview question.** *What do you do when the data cannot answer the
question you were asked?*
Say so, and say precisely what it can answer instead. Not being able to measure something is
usually the more actionable finding, because it names a gap in the record rather
than producing a number nobody can act on.

## Phase 6. The site

**What we did.** Built four pages of plain HTML, CSS and JavaScript with no
framework and no build step. Every figure is injected at load time from
`docs/data/`. No number is typed into the markup, and a test enforces it.

**Why it matters.** A number typed into a page is a number that drifts from its
source the moment the source changes. That is not theoretical: it happened five
times on this project, and is the tenth judgment call in the README.

**New terms.**
- **Single source of truth.** One place a fact is stated. Everywhere else reads
  it. A correction applied to the source cannot survive in a copy.
- **Cache busting.** Appending a content hash to an asset address so a browser
  fetches the new version instead of serving the old one.

**Decisions the owner made, and why.** The design view leads and the findings
follow as evidence, because the ordering is the argument. A figure reaches the
landing page only if its qualification survives being shortened to one line
that still holds. The ones that do not are linked rather than reduced.

**Interview question.** *How do you keep a published figure correct over time?*
Compute it once, publish it from that single place, and test that nothing
restates it. If a person can retype a number, a person eventually will, and
nothing on the page will look broken when they do.

## Phase 7. Safeguard review

**What we did.** Ran the full suite, then ran the checks no test can perform: a
reading for trend framing, a reading for source attribution, a reading for the
absence of any claim about who wrote the code, and a reading of every heading
against the figure beneath it.

**Why it matters.** A test verifies wording, structure and provenance. It cannot
verify that a claim matches its evidence, because that means holding both in
mind and asking whether they agree. The heading reading found three claims that
said more than the thing beneath them supported. The suite was green throughout.

**New terms.**
- **Manual check with a named owner.** An untested gap with a named owner and a
  stated trigger is a control. The same gap without one is a hope.
- **Planting the failure.** Verifying a test by breaking the thing it exists to
  catch, rather than trusting that a passing test was ever able to fail.

**Decisions the owner made, and why.** Prose corrections come to the owner.
Numeric ones are corrected and reported. A published figure that does not match
the data is a defect and should not be held pending a conversation.

**Interview question.** *Your automated checks are all green. What does that
tell you?*
That the things somebody thought to test are holding. It says nothing about the
claims in the prose around the numbers. On this project every published figure
was correct by the tests while four of them were wrong, because no test
compared a published number to the data until one was written for it.

## Phases 8 and 9. README, deployment, and two things withdrawn

**What we did.** Wrote the README as a case study, published the site from
GitHub Pages, and recorded ten judgment calls including the ones that went
badly.

Two things were built and then withdrawn. A second surface for the findings,
built as a separate application, was moved into this repository when the
separate one could not be created, and then dropped entirely because it could
not carry the design the site carries. A social preview card was built and then
removed at the owner's request. Both decisions are recorded with their reasons
rather than deleted.

**Why it matters.** The record of a decision that was reversed is worth more
than the absence of it. A reader can see what was weighed. Deleting the history
of a reversal leaves a project that looks like it never had to choose.

**New terms.**
- **Scope lock.** A written statement of what the project is not, so that
  adding something requires a decision rather than a drift.
- **Unreachable is not deleted.** Rewriting published history makes old commits
  unreachable from a branch. The host keeps the objects until it collects them,
  and anything computed from them keeps showing.

**Decisions the owner made, and why.** The application was dropped because it
stated the same findings less well than the site, which is the same objection
this project makes to a figure lifted away from what qualifies it. The reasoning
was kept in the decision record, because a record that deletes its own history
is not a record.

**Interview question.** *Tell me about something you built and then removed.*
A second surface for the findings. It worked and it passed its checks, but it
could not carry the parts of the design that do the explaining, so it was a
weaker copy of something that already existed. The cost of keeping it was a
looser scope lock and a safeguard enforced by a test where it had previously
been enforced by the data simply not being there. Removing it was cheaper than
maintaining a second, worse version of the same argument.
