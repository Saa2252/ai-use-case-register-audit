"""The proposed field set for page four.

Page four is the author's own design view. It is not a claim about what any
publisher should ask. Two rules hold that line and both are enforced here:

1. **Every field traces to a finding.** A field that cannot be traced to
   something the audit established does not go on the page. The `finding` key
   is required and is checked by a test.
2. **Whether either real register already asks it is stated**, so a reader can
   see which parts are new and which already exist somewhere.

Wording rule: each field says what it records. None says what a register ought
to ask. Any line that crosses that is flagged to the owner rather than shipped.
"""

from __future__ import annotations

FIELDS = [
    {
        "name": "Entry identifier",
        "records": "A reference code that stays the same for this entry from one year to the next.",
        "finding": "Of 3,611 entries, 706 carry no usable identifier, and the earlier year's list "
                   "carries none for any entry, so no entry can be followed between the two.",
        "finding_link": "index.html",
        # {repeated_ids} is filled in by scripts/build_fieldset.py from the
        # published findings. It was typed as "thirteen" and the file says
        # twelve, so it is no longer written out here.
        "us_2025": "Asks for one. It is filled on four fifths of entries, and {repeated_ids} "
                   "values appear on more than one row.",
        "ontario": "Does not ask.",
    },
    {
        "name": "Date this entry was last checked",
        "records": "The date a person last confirmed that this entry still describes the system.",
        "finding": "Nothing in the register records when an entry was checked. Its single date "
                   "field records when a system started running, which answers a different question.",
        "finding_link": "gaps.html",
        "us_2025": "Does not ask.",
        "ontario": "Does not ask.",
    },
    {
        "name": "What changed since the last check",
        "records": "Which of a named set of changes has happened since the entry was last "
                   "confirmed: the responsible office, the model or its version, the data it "
                   "draws on, what it is used for, or how far it acts without a person.",
        "finding": "Five kinds of change would normally call for an entry to be verified again. "
                   "No field in the register records any of them as a change, and one of the "
                   "five is not present in the field set at all.",
        "finding_link": "gaps.html",
        "us_2025": "Does not ask.",
        "ontario": "Does not ask.",
    },
    {
        "name": "Acts without a person reviewing the output",
        "records": "Whether the system can carry out a decision or action without a person "
                   "looking at its output first.",
        "finding": "The 2025 federal register does not ask this question. The Ontario "
                   "register asks it as a standing field.",
        "finding_link": "gaps.html",
        # This field has one source and that source is small. The owner ruled on
        # 30 September 2026 that the limit is stated here, at the point of use.
        "rests_on": "{{ontario_is_three}}",
        "us_2025": "Not present in the 2025 field set.",
        "ontario": "**Asks it**, as a standing field.",
    },
    {
        "name": "Where a person reviews it",
        "records": "The point in the process at which a person sees the output, if there is one.",
        "finding": "The 2025 federal register does not ask this question. The Ontario "
                   "register asks it as a standing field.",
        "finding_link": "gaps.html",
        # This field has one source and that source is small. The owner ruled on
        # 30 September 2026 that the limit is stated here, at the point of use.
        "rests_on": "{{ontario_is_three}}",
        "us_2025": "Not present in the 2025 field set.",
        "ontario": "**Asks it**, as a standing field.",
    },
    {
        "name": "Impact classification, with an explicit option for not yet assessed",
        "records": "How seriously the system is rated, including a value meaning no assessment "
                   "has been made, so that an unassessed entry is distinguishable from a blank.",
        "finding": "The classification field has four states in practice, and the fourth is that "
                   "nothing was recorded: 426 entries carry no classification at all, which is "
                   "more than the 110 assessed and set aside.",
        "finding_link": "obligations.html",
        "us_2025": "Asks it. The options do not include one meaning no assessment was made.",
        "ontario": "Does not ask.",
    },
    {
        "name": "Withheld from public reporting, and on what ground",
        "records": "Whether any part of this entry is held back from publication, and if so on "
                   "what ground. Named in the direction the question is asked, so that an answer "
                   "of no means nothing was held back.",
        "finding": "The field asking whether an entry should be withheld is required, and is "
                   "blank for 274 of the 445 entries flagged high-impact.",
        "finding_link": "obligations.html",
        "us_2025": "Asks it, and requires an answer.",
        "ontario": "Does not ask.",
    },
    {
        "name": "The nine oversight questions, each with its own explicit states",
        "records": "Each carries its own answer, including one meaning the question does not "
                   "apply. They are nine fields, not one.",
        "sub_fields": [
            "Tested before deployment",
            "Impact assessment completed",
            "Potential impacts identified",
            "Independent review conducted",
            "Ongoing monitoring in place",
            "Training established for operators",
            "Fail-safe in place",
            "Appeal process in place",
            "Consultation with the people it affects",
        ],
        "finding": "Of 445 high-impact entries, 126 answer all nine and 317 answer none, with "
                   "two in between. The nine arrive together or not at all.",
        "finding_link": "obligations.html",
        "us_2025": "Asks all nine. Two of them offer a not-applicable option.",
        "ontario": "Does not ask.",
    },
    {
        "name": "What this entry counts as one of",
        "records": "Whether this entry describes one system, or a class of common tools reported "
                   "together, so that a reader knows what a count of entries is a count of.",
        "finding": "The register publishes two routes that count different things and cannot be "
                   "added: 3,611 systems reported individually, and 45 agencies reporting against "
                   "21 common tasks.",
        "finding_link": "gaps.html",
        "us_2025": "Implied by publishing two separate files, not recorded in either.",
        "ontario": "Does not ask.",
    },
    {
        "name": "Who completed this entry, and when",
        "records": "The office that filled this entry in, and the date it did so.",
        "finding": "How completely an entry is filled in varies far less within one agency's "
                   "submission than across the register, and the nine oversight fields arrive "
                   "together or not at all. What produces that pattern cannot be read "
                   "from the file, because it records nothing about who filled an entry "
                   "in or when.",
        "finding_link": "gaps.html",
        "us_2025": "Does not ask.",
        "ontario": "Does not ask.",
    },
]

# A rule the whole field set follows. It is not one of the fields, and it is not
# numbered with them, because it governs how every one of them records an
# absence rather than recording anything itself.
EMPTY_CONVENTION = {
    "name": "Every field records an empty answer the same way",
    "records": "Every field distinguishes four states: answered, the question does not apply, "
               "not yet answered, and withheld. No field records an absence as ordinary text.",
    "finding": "Two fields store an empty answer as a pair of brackets a spreadsheet counts as "
               "content; words such as 'No' and 'Not available' record an absence in one field "
               "and a real answer in another; the development stage field offers four answers "
               "with no option meaning nobody filled it in; and a value the file uses appears "
               "nowhere in the document describing the field.",
    "finding_link": "gaps.html",
    "us_2025": "No single convention. Three of the seven counting problems on the gaps page "
               "come from how an empty answer is recorded.",
    "ontario": "Not enough published entries to tell.",
}


# --- The evidence strip -----------------------------------------------------
#
# The caveat test, set by the owner: a figure goes here only if its
# qualification survives being shortened to a line that still holds. A figure
# that cannot carry its qualification in one line stays in the site as normal
# and is reached through a link to its section, never reproduced here as a
# number.
#
# Each entry records the shortened qualification that was tested, so the test
# can be re-read rather than taken on trust.

EVIDENCE = [
    {
        "path": "M4.oversight_block_shape.none_answered",
        "of": "M4.subset_size",
        "reads": "of the entries flagged high-impact have all nine oversight fields empty",
        "caveat": "A filled field shows information was provided, not that the practice is adequate.",
        "link": "obligations.html",
    },
    {
        "path": "R3.figures.rows_with_no_usable_identifier",
        "of": "M1.individually_reported_entries",
        "reads": "entries carry no usable identifier",
        "caveat": "The register asks for one, and permits agencies to remove the column from their own inventories.",
        "link": "register.html",
    },
    {
        "path": "M4.withholding_status.high_impact_with_no_status",
        "of": "M4.withholding_status.high_impact_entries",
        "reads": "high-impact entries say nothing about whether they were withheld",
        "caveat": "A blank is not evidence anything was withheld. The field is required.",
        "link": "obligations.html",
    },
    {
        "path": "M4.bands.classification not recorded",
        "of": "M4.register_rows",
        "reads": "entries carry no impact classification at all",
        "caveat": "No inference is drawn in either direction.",
        "link": "obligations.html",
    },
    {
        "path": "M3.operational_date.usable_dates_as_share_of_all_rows",
        "suffix": "%",
        "reads": "of entries carry a date that can be read reliably",
        "caveat": "It records when a system started running, not when the entry was checked.",
        "link": "gaps.html",
    },
]

# Figures that did not pass the test. Linked to, never reproduced as a number.
EVIDENCE_WITHHELD = [
    {
        "name": "How many entries resemble each other",
        "why": "It is three numbers, not one. The finding is that the count triples depending on "
               "where the line is drawn, so any single figure states the opposite of what was found.",
        "link": "gaps.html",
    },
    {
        "name": "How completeness varies within an agency against across the list",
        "why": "Its qualification shortens cleanly, but the figure does not stand alone: a median "
               "of two against fifteen means nothing without the setup that precedes it. "
               "Kept out of the strip for that reason, and linked instead.",
        "link": "gaps.html",
    },
]
