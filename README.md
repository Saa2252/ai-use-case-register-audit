# AI Use Case Register Audit

> This is an independent portfolio project. It uses publicly available AI use case inventories published by the US Office of Management and Budget (public domain, 17 U.S.C. §105) and the Government of Ontario (Open Government Licence – Ontario). Vendor and product names have been removed. Findings describe patterns in the published data and are not claims about any agency's conduct. This is not legal advice. Not affiliated with or endorsed by any government body.

**Live site:** https://saa2252.github.io/ai-use-case-register-audit/

**Repository:** https://github.com/Saa2252/ai-use-case-register-audit

**The application:** a single page at `app/app.py` that puts the design view
and its evidence together. Run it with `streamlit run app.py` from the `app`
directory. It reads `data/derived/` directly, so it holds no copy of any
finding, and it offers no way to filter or sort by agency. Both points, and
what the second one cost when the application moved into this repository, are
recorded in `governance/decision-rules.md` section 23.

## What this is

**This project takes a list that a government publishes of its own AI systems, reads it the way someone responsible for overseeing those systems would have to, and reports what the list can and cannot answer.**

It examines 3,611 entries published by US federal agencies in 2025, alongside a second and much smaller list published by the Government of Ontario. Both were downloaded on one day and recorded by hash, so everything here describes those exact files and can be checked against them.

The work is the audit. The governance design, the rules it follows and the judgments in it are the author's.

**Ontario data.** Contains information licensed under the Open Government Licence – Ontario. The licence is at <https://www.ontario.ca/page/open-government-licence-ontario>.

## Why a list like this exists at all

An organisation cannot oversee what it has never written down. That is the whole idea behind an AI use case inventory, usually just called a register: a published list of the AI systems an organisation uses, so that anyone responsible for them knows what there is.

Several governments now require one. The United States requires federal agencies to publish theirs, and this project reads the 2025 edition.

The interesting question is not whether a register exists. It is whether the register can answer the questions people will actually put to it. That is what this project tested.

## What was examined

| | |
|---|---|
| **The main list** | 3,611 entries published by 41 US federal agencies in 2025 |
| **A second route in the same publication** | 45 agencies reporting against 21 common tasks, counted separately and never added to the first |
| **A second government's list** | 3 entries published by the Government of Ontario, used only to compare what each list asks |
| **An earlier edition** | The 2024 US list, used only to compare which questions each year asks. Its rows are not read |
| **Downloaded** | On one day, each file recorded by SHA-256 hash |

Everything published here is computed from those files by one notebook and written to `data/derived/`. No number on the site is typed in by hand.

## What the audit found

Five questions, and what the register could answer.

**Is the same system registered once, or more than once?** The list counts two different things that cannot be added together: systems reported individually, and agencies ticking common tasks on a shared list. Entries that read alike can be found by comparing wording, but how many depends entirely on how alike they must be, so the number is a choice rather than something the file contains.

**Is the register complete, and does it add up?** Four of the seven figures the publisher states match the data exactly. Three do not, and the publisher's own summary table disagrees with the total printed beneath it. How completely an entry is filled in varies far more between agencies than within one.

**How current is any of it?** It cannot be known. The register records no date on which an entry was checked. Its single date field records when a system started running, which answers a different question.

**Could it answer an oversight request?** The register sets aside nine fields about human oversight for its most serious entries. Of the 445 flagged high-impact, 317 have all nine empty, and 274 carry nothing in the field asking whether the entry should be withheld from public reporting.

**What does a second government ask that this one does not?** Ontario asks, as standing questions, whether a system acts autonomously and whether a person is in the loop. Neither is present in the 2025 US field set. Ontario names no vendor in any published field.

Each finding on the site carries its own qualification, visible on the page, and every figure links to the working behind it.

## The decisions that shaped it

Most of what determines these numbers is not technical. It is a set of rules decided before the analysis ran, written down, and then applied. The full record is in `governance/decision-rules.md`. The ones that changed the most:

**What counts as one use case.** One row is one entry. Nothing is merged, no total is adjusted, and entries that resemble each other are flagged as candidates and never treated as confirmed. All three similarity settings are published together, because publishing one would hide that the number is a choice.

**The two years are never compared at row level.** The earlier list was reclassified partway through as a reference for its questions only. Its rows are not read. The category defining serious entries was rewritten between the two years under a different memorandum, the rules for what to include changed, and the earlier file carries no identifier for any entry. Any comparison would describe the rules rather than the world.

**Freshness became a finding rather than a measure.** The original plan was to rate how current each entry was. The data cannot support it, so the project reports that instead, and reports which of five events that would normally prompt a re-check the register could detect. It can detect none of them.

**No trend, anywhere.** No count in this project is presented as movement over time. A list of words enforcing that is checked automatically, and a person reads for the same thing in sentences that use none of them.

**Nothing describes conduct.** Findings describe the file. An empty field is reported as an empty field, never as an omission by the organisation that published it.

## How this project handled ten judgment calls

### A test that did not pass, and the wrong way to fix it

A safeguard test checks that no vendor or product name appears in the published
data or on the site. During the scrubbing phase it did not pass, because two
company names collided with ordinary web page structure: one shares its name with a
standard HTML tag, the other with a stylesheet keyword.

The quick fix was to take those two names off the list the test checks against.
That was done, and the test passed.

Checking the output afterwards showed both companies still named in the
published register, one of them inside a link to a company research page.
Removing a term from the list a test reads is not fixing the problem. It is
editing the evidence, and it had left a real gap in place.

Both terms were restored, the data was scrubbed again, and the part that was
genuinely a false positive was escalated rather than engineered away. The
project's rules say a test is never weakened to make it pass. The rule worked
here only because the output was checked after the test went green, which is the
practical lesson: a passing test is a claim, not a result.

### Stating what a control does not cover

The automated check on vendor names verifies something narrower than its name
suggests, and saying so plainly was a decision rather than an oversight.

The list of names to remove is built from the field where an agency is asked to
name its supplier. The check then confirms that nothing on that list survives in
the published data. What it cannot confirm is that no company or product name
survives at all, because an agency may mention a product only in a paragraph of
description and never enter it in the supplier field. Several such products were
found by reading and were added to the list by hand, which shows the category is
real rather than that it has been emptied.

That gap could be pursued. Doing so would mean identifying every commercial name
written in free text by 41 organisations across more than three and a half
thousand entries, with no field listing them and no way to know when the work
was complete. Each pass would find more, which is the same objection that led
this project to replace its redaction method rather than keep patching it: an
obligation with no natural endpoint is not a control, and presenting it as one
is worse than stating a narrow control's boundary.

So the boundary is stated. This project claims that no term on its list survives
in what it publishes. It does not claim that no vendor name survives anywhere,
and nothing here should be read as making that claim.

### Drifting into an approach nobody chose

The most useful thing this project demonstrated is not a finding about the data.
It is what happened to its own method while nobody was counting.

Removing company and product names from a public register sounds like a single
task. In practice it produces a steady supply of individual cases: a word that
is both a company and an ordinary noun, a company name that collides with a
standard piece of web page structure, a government system that an agency typed
into the field asking for its supplier. Each case arrives with an obvious local
fix, and each fix is defensible on its own.

By the time the method was examined as a whole, the following had accumulated:

| | Count |
|---|---|
| Terms held back from the list because they are also ordinary words | 9 |
| Terms restored after checking showed the first decision was wrong | 3 |
| Casing carve-outs applied to individual terms | 2 |
| Exemptions added to the automated test | 3 |

Not one of those was unreasonable when it was made. Together they were an
approach, and it was an approach nobody had chosen, written down, or agreed.
Asked to state the rule for whether a given word would be removed, the honest
answer would have been that it depended on which decision had been made about
that word, and where that decision was recorded.

The cheapest way forward was to carry on: keep the method and add exceptions as
reviews turned them up. That option was considered explicitly and refused, for
one reason above the others. **It has no natural stopping point.** The method
generates the cases, so reviewing finds more, and the list of exceptions grows
for as long as anyone keeps looking. There is no state in which that work is
complete, only a state in which nobody is currently checking.

The method was replaced instead: candidate terms are now taken only from the
field where an agency names its supplier, and every term that can affect the
published text was then checked individually and recorded. The count above is
the reason, and the count is the only way the problem was visible at all. No
single decision in it looks like a problem.

### The project's own writing kept breaking its own rules

The word lists were written to stop this project describing organisations badly.

**Counting only sentences written for this project that used a word on one of
its own lists**, wherever those sentences appear: on the three pages, in this
document, in the governance records, or in a comment inside the code. It has
happened **eleven times**, and no agency has tripped them once.

This note cannot quote the offending sentences, because quoting them would break
the same rules again. It describes them instead.

| # | What the sentence was trying to say | Where |
|---|---|---|
| 1 | That a caveat sits in the open rather than out of sight behind a click | A findings page |
| 2 | That two yearly counts are not presented as movement in either direction | A findings page |
| 3 | That dropping a figure without a word would have left no trace of the decision | This document |
| 4 | A heading for a note about a test that did not pass | This document |
| 5 | That an entry named after a medical prediction tool frames nothing | The safeguards record, inside the paragraph explaining why movement words are banned |
| 6 | That a table of entries imposes no ordering on them | A findings page |
| 7 | This note's own first draft, which set the offending phrases out in a table | This document |
| 8 | That scope can expand within a page | The safeguard review |
| 9 | A comment explaining how a collision with page markup had been avoided | The site's own code |
| 10 | That two entries out of hundreds sit between two states | A findings page |
| 11 | That an empty field is never reported as an omission by anyone | This document |

Six of the eleven share a shape: **a sentence denying something, using the word
for the thing it denies.** Stating that a figure did not move puts the word for
movement on the page, and a word list cannot read the "not".

Every one was reworded rather than exempted, and every rewording was better than
what it replaced. Saying a caveat is tucked behind a click is plainer than the
word it replaced. Saying an order carries no judgment about the entries says
more than denying a comparison, because it describes what is absent instead of
naming a thing and pushing it away.

The wider point is about who a control is for. These lists were built to govern
how this project describes other people's work. In practice they governed this
project's own writing, because that is the only writing the project controls. A
rule that only ever binds someone else is not a control, it is an opinion.

### A heading that claimed the opposite of the finding beneath it

One section of this site was headed **"Most entries cannot be followed from one
year to the next"**. Directly beneath it stood the finding: 706 entries out of
3,611 carry no identifier.

706 of 3,611 is under a fifth. The heading did not overstate the finding. It
claimed the opposite of it, on the same screen, a line apart.

It passed every test in the suite. It survived several readings of the page. It
was found during a deliberate pass over every heading on the site, asking one
question of each: does the heading claim more than the thing under it supports.

The reason it survived is worth being precise about. **The sentence was
grammatical, used no word on any banned list, made no comparison between
organisations, stated no legal conclusion, and drew no inference about an empty
field.** Every rule this project wrote was satisfied. The tests check how a
claim is worded, whether required text is present, and where a number came
from. Not one of them reads the claim and the evidence together.

That check has no automated form. A test can confirm that a figure came from the
notebook. It cannot confirm that the sentence above the figure describes it.
Doing that means holding the claim and the evidence in mind at once and asking
whether they agree, which is reading.

The lesson is not that the tests are weak. They caught things a reader would
never have found: a company name inside a link, a rule that had drifted by seven
values, three of this project's own sentences breaking its own rules. The lesson
is that a test suite has a shape, and the shape here is that it verifies
**wording, structure and provenance**. Whether a claim matches its evidence sits
outside that shape entirely, and a project that does not notice the difference
will mistake a green suite for a checked document.

The check is now recorded alongside the reading that covers neutral language,
with the same named owner and the same trigger: it is repeated whenever
published copy changes.

### A rule written down twice drifted immediately

The project defines what counts as an empty value: a blank cell, but also the
words and characters a form uses to record that there is nothing to give. That
rule decides every completeness figure published here, so it lives in one file
and everything reads it from there.

Except that when the register's detail panel was built, the rule was written out
again inside the page's own code, because that was quicker than fetching it.

The two copies were identical on the day they were written. They did not stay
that way. **The rule held twenty-eight values. The copy held twenty-one.** Seven
values counted as empty in every published figure while the page displayed them
as raw text, so the same entry reported one thing in a number and another thing
on screen.

Nothing caught it. Not the test suite, not a review of the code, not a reading
of the page. It surfaced because the owner opened one ordinary entry, saw two
fields showing a pair of brackets where every other blank field said "blank",
and asked why.

Three things are worth taking from it.

**The second copy was invisible.** Nobody looking at either file would see a
problem. Both were correct on their own terms. The defect existed only in the
relationship between them, and nothing in the project was looking at that.

**It drifted at the first change.** Not after months. The rule gained seven
values in the ordinary course of the work, and the copy did not, because nobody
remembered it existed.

**Checking one real record by hand found what automation had not.** That is not
an argument against the tests. It is an argument for keeping one thing in the
work that a person does directly, on real data, without tooling in between.

The rule is now fetched rather than restated, a script publishes it from the
single source, and a test fails if any page code sets out a list of emptiness
values again. An audit of the rest of the project's rules followed, and is
recorded with this note in the project's governance documents.

### What happens when a word test meets text nobody wrote as prose

**Counting only matches against text nobody wrote as prose**, which is the other
category entirely, a word list applied across a repository will keep meeting
markup, code and data. That has happened **five times**, and the resolution
differs by what the match actually was.

| What was matched | What it really was | What was done |
|---|---|---|
| A company name inside a required character-set declaration | Markup a browser needs | An exemption naming that exact string |
| A reserved word used as an attribute on a page control | Markup | **Rewritten** so the collision no longer exists |
| The same attribute name, later, on the panels behind the section tabs | Markup | **Rewritten** the same way |
| A reserved word used as a variable name in the site's code | A code identifier | **Renamed**, so no exemption was needed |
| Movement words inside agency-authored entry names | Source data | A scope statement, drawn by field rather than by file |

This is a property of the method, not a run of bad luck. The third case arrived
the day after the pattern was written down, and the fifth is the second case
happening again in a different part of the page.

So the question each time is one question: **is the match this project's own
writing?** If it is, the copy changes. If it is not, the first choice is a fix
that removes the collision outright, and only failing that a scope statement,
recorded where someone can audit it.

What is never acceptable is the fourth option, which is to take the term off the
list the test reads. That makes the test pass while leaving the thing it was
checking for exactly where it was. It was tried once here and reversed, and it
is the first note above.

### Two ways the right data still reached the reader wrong

Both were found by someone reading the page rather than by any test, and both
sat in the gap between what the system held and what appeared on screen.

**A label built from a database column name.** The register names its columns for
a machine: `has_pii`, `have_ato`, `hi_public_consultation`. The site turned those
into labels by taking the underscores out, which is the obvious thing to do and
works for most of them. For one it did not. The prefix `hi_` marks the nine
questions asked only of entries flagged high-impact, so that column reached the
reader as **"hi public consultation"**, which reads as a greeting.

The fix was to stop deriving labels and start looking them up: every published
column now has a plain label written once and fetched by the page. A test rejects
any script that builds a label out of a column name.

It also surfaced something the underscores had been hiding. That prefix carried
meaning, and replacing it with readable words dropped it: a reader seeing
"Consultation with the people it affects" could not tell it is asked only of the
most serious entries. Those fields are now introduced by the condition they are
asked under, stated once above them. Writing that out showed the justification
field belongs to a different condition again, asked only of entries presumed
serious and then judged not to be, which is a different population from the nine
and is now a separate group.

**A correction that arrived after the first paint.** The labels are fetched, so
for a moment the page drew the old raw names and then redrew with the right ones.
Every test passed, because by the time anything measured the page it was correct.
A reader who looks quickly, or takes a screenshot, sees the wrong state, and has
no way to know it was ever going to change.

Anything that prints a label now redraws when the labels arrive. The general
lesson is narrow and worth keeping: **a page that is correct only after an
asynchronous step is a page that is wrong to whoever reads it fast.** Testing the
settled state proves less than it appears to.

### A figure that was produced and not published

One figure produced during the analysis was not published.

A method for matching entries between the two years was tested and rejected,
because the matching key is not unique within a single year and so cannot be
one-to-one in either direction. The test produced an overlap figure. That figure
presents as a rate of entries carried between years, which is a conclusion the
method cannot support.

It was escalated to the owner rather than published with a caveat or quietly
dropped. Publishing it with a caveat would have put the number into circulation,
where the caveat does not travel with it. Dropping it silently would have left no
record of the decision. The reasoning is recorded in `governance/decision-rules.md`.
### A rule enforced in one place and typed by hand everywhere else

Safeguard S5 says every number on the site is computed by the analysis and
loaded from `data/derived/`. An audit of every published figure against the raw
file found **four numbers that were wrong**.

| Where | Published | The file holds |
|---|---|---|
| Two pages, on identifier repeats | thirteen | 12 |
| The register page, on entries with no identifier | a sixth | 19.6%, which the heading above it called nearly a fifth |
| The gaps page, under a heading reading "Seven ways" | these six | seven |
| The gaps page, on the size of an error | about seventy percentage points | 69.4 on one field and 92.7 on the other, both printed beneath it |

A fifth figure, a count of agency submissions, was published with no working at
all and could not be reproduced by any method. It has been removed and replaced
with a statement that it could not be reconciled, with every method tried
recorded in `governance/data-provenance.md`.

**Every one of them was typed by hand.** None came from the analysis. The
evidence strip on the landing page obeys S5 and resolves its figures from the
findings; the prose around it did not. The rule existed, was documented, was
enforced in one place, and was ignored everywhere else. A rule enforced in one
place and typed by hand everywhere else is not a rule. It is a habit that
happens to hold in the place someone checked.

**The part that matters is that this was already known.** An earlier note in
this file, *A heading that claimed the opposite of the finding beneath it*,
recorded exactly this lesson: the test suite verifies wording, structure and
provenance, and does not verify that a claim matches its evidence. That was
written down, and nothing was built to act on it. The same class of error then
recurred four more times, in four different files, over the following week.
Writing a lesson down is not the same as closing it. A finding that produces no
test produces nothing.

At the point the audit ran, the suite held 42 tests. Not one compared a
published number against the data.

**What closed it.** `tests/test_published_claims.py` recomputes nine figures
from the raw file and fails naming any that have drifted, and checks the two
specific counts that were wrong against the file rather than against another
page. `tests/test_single_source_statements.py` fails if a page writes out a
shared fact instead of taking it from `src/statements.py`, which is the same
defect in a second form: a sentence corrected on one page had survived
unchanged on another because each page stated it independently. Both were
verified by planting the failure they exist to catch.

**What it cost to find.** Nothing on the site was visibly broken. Every page
rendered, every test passed, every caveat was present and every link resolved.
The errors were only reachable by recomputing each published figure from the
raw file and comparing. A suite that is green says the things it checks are
true. It says nothing about the things it does not check.

## What this project cannot show

This is the part that took the longest to get right.

- **Anything that was never written down.** A published list shows what was declared. Nothing here says anything about systems nobody recorded.
- **Whether anything is adequate.** A filled field shows that information was provided. It does not show that the practice described is any good. An empty field is not evidence that the practice is absent.
- **Whether two similar entries are the same system.** Comparing wording cannot establish it, and the count of similar entries triples depending on where the line is drawn.
- **Anything about change over time.** The two editions ask different questions, define their central category differently, and the earlier one carries no identifiers. They are not two readings of one ruler.
- **How any agency actually works.** Everything here is read from outside, from one published file, downloaded on one day.
- **That no vendor name survives.** The automated check verifies that no term on its list survives. It cannot verify that no vendor name survives, because commercial names appearing only in narrative text are outside that list by construction. The boundary is stated rather than quietly assumed.

## Reproducing it

```
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements-analysis.txt
./.venv/bin/python -m pytest
./.venv/bin/python -m jupyter notebook notebooks/analysis.ipynb
```

Two dependency files, because two things run here. `requirements-analysis.txt`
holds the pins that reproduce the numbers. `requirements.txt` holds the single
package the deployed application needs, and sits at the root because that is
where the host serving the application looks.

Raw data is deliberately not committed. The raw files carry vendor and product columns, and committing them would break this project's own rule against publishing vendor names. The notebook downloads each file from its official address and checks it against the hash recorded in `governance/data-provenance.md`, so the results reproduce without the repository ever holding a vendor name.

Any single entry can be checked against the file it came from:

```
./.venv/bin/python scripts/verify_entry.py CFTC-003
```

That prints the raw row as downloaded, compares it field by field with what the site publishes, and shows the completeness working.

## How it is put together

| Path | What it holds |
|---|---|
| `governance/safeguards.md` | Twelve rules every published file obeys, the test enforcing each, and what each test does not cover |
| `governance/decision-rules.md` | Every rule decided by the owner, in the owner's words, with the reasoning |
| `governance/data-provenance.md` | Where every file came from, when, its hash, and what its fields mean |
| `governance/phase7-review.md` | The safeguard review, and the checks no test can perform |
| `notebooks/analysis.ipynb` | Download, verify, scrub, analyse, export |
| `data/derived/` | Everything published. Every figure on the site comes from here |
| `docs/` | The site |
| `tests/` | 30 automated checks, run with pytest |

## Licence

MIT, covering the code only. The source data carries its own licences, recorded in `governance/data-provenance.md`.

Governance design by Sana Ahmad.
