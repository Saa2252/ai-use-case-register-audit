"""Plain labels for the register's own column names.

The published file names its columns for a database, not for a reader. Shown
with the underscores taken out, one of them reads as a greeting: the prefix
"hi_" marks the nine questions asked only of high-impact entries, so
hi_public_consultation renders as "hi public consultation".

These labels say what each column holds, in the words the publisher's own data
dictionary uses, shortened to fit a table. The raw column name stays in the
data for anyone matching against the source file.
"""

FIELD_LABELS = {
    "agency": "Agency code",
    "agency_name": "Agency",
    "id": "Entry identifier",
    "use_case_name": "Use case name",
    "agency_bureau": "Bureau or component",
    "is_withheld": "Withheld from public reporting",
    "development_stage": "Development stage",
    "is_high_impact": "Impact classification",
    "HI_justification": "Justification for that classification",
    "topic_area": "Topic area",
    "classification": "Type of AI",
    "problem_solved": "Problem it is intended to solve",
    "benefits": "Expected benefits",
    "system_outputs": "What the system produces",
    "operational_date": "Date it became operational",
    "contracting_usage": "Bought from a vendor, or built",
    "have_ato": "Has an authorisation to operate",
    "data_description": "Data used to build or evaluate it",
    "link_to_data": "Link to that data",
    "has_pii": "Involves personal information",
    "pia_url": "Link to the privacy impact assessment",
    "demographic_features": "Demographic variables the system uses",
    "has_custom_code": "Includes custom-written code",
    "code_url": "Link to the source code",
    # The nine oversight questions, asked only of high-impact entries.
    "hi_testing_conducted": "Tested before deployment",
    "hi_assessment_completed": "Impact assessment completed",
    "hi_potential_impacts": "Potential impacts identified",
    "hi_independent_review": "Independent review conducted",
    "hi_ongoing_monitoring": "Ongoing monitoring in place",
    "hi_training_established": "Training established for operators",
    "hi_failsafe_presence": "Fail-safe in place",
    "hi_appeal_process": "Appeal process in place",
    "hi_public_consultation": "Consultation with the people it affects",
}


# Some columns are only ever asked under a condition, and the condition is part
# of what the field means. The register carries that in a prefix on the column
# name, which is lost the moment the name is replaced with a readable label.
#
# Grouping is used rather than prefixing each label. Nine of these appear
# together in a table whose heading already names the condition, and repeating
# "High-impact:" nine times down that column adds noise without adding meaning.
# The group is stated once, above them, wherever they appear.
#
# The justification field sits in its own group. Its condition is different: the
# dictionary specifies it only when an entry is presumed high-impact and then
# determined not to be, which is not the same population as the nine.
FIELD_GROUPS = {
    "high_impact_oversight": {
        # The register's own dictionary: "Required: Yes, only for high-impact
        # deployed use cases". Saying only the first half of the condition is
        # what let every figure below it be divided by 445.
        "label": "Asked only of entries that are flagged high-impact and deployed",
        "columns": [
            "hi_testing_conducted", "hi_assessment_completed", "hi_potential_impacts",
            "hi_independent_review", "hi_ongoing_monitoring", "hi_training_established",
            "hi_failsafe_presence", "hi_appeal_process", "hi_public_consultation",
        ],
    },
    "presumed_not_high_impact": {
        "label": "Asked only when an entry is presumed high-impact and then determined not to be",
        "columns": ["HI_justification"],
    },
}

GROUP_OF = {
    column: group["label"]
    for group in FIELD_GROUPS.values()
    for column in group["columns"]
}


def label(column: str) -> str:
    """The reader-facing label, falling back to the column name if unmapped."""
    return FIELD_LABELS.get(column, column)


def group_of(column: str) -> str | None:
    """The condition under which this column is asked, if it has one."""
    return GROUP_OF.get(column)
