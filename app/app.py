"""What a published AI register can and cannot answer.

The application. A second surface for this project's findings, approved by the
owner on 30 September 2026 as a scope change and recorded in
governance/safeguards.md.

It reads `data/derived/` directly, which is the same single source the site
reads. There is no copy of the findings anywhere in this application, so there
is nothing that can drift out of step with a correction.

Two rules govern this file and are worth stating at the top of it.

Every figure shown here is read from those files. No figure is typed into this
page. The audit's S5 says a published number is computed and loaded, and that
rule travels with the numbers rather than staying behind with the site.

There is no agency filter and no agency sort, by the owner's ruling of
29 September 2026. A page honours the no-comparison safeguard by choosing what
to publish. An application with a filter cannot, because the reader assembles
the comparison themselves, out of data that does not support it. The files this
application loads carry no per-agency rows at all, so the comparison cannot be
built here even by mistake.
"""

import json
from pathlib import Path

import streamlit as st

DATA = Path(__file__).resolve().parent.parent / "data" / "derived"

SITE = "https://saa2252.github.io/ai-use-case-register-audit/"
REPOSITORY = "https://github.com/Saa2252/ai-use-case-register-audit"

# How the audit's four page names map to the live site, so a link recorded in
# the findings resolves rather than pointing at a filename.
PAGES = {
    "index.html": SITE,
    "register.html": SITE + "register.html",
    "gaps.html": SITE + "gaps.html",
    "obligations.html": SITE + "obligations.html",
}


@st.cache_data
def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def n(value) -> str:
    """Group a count the way every other surface in this project groups one."""
    return f"{value:,}" if isinstance(value, int) else str(value)


def link_for(target: str) -> str:
    return PAGES.get(target, SITE)


def measure(findings: dict, name: str) -> dict:
    for item in findings["findings"]:
        if item.get("measure") == name:
            return item
    return {}


# --- the page ---------------------------------------------------------------
# set_page_config has to be the first Streamlit call in the script, which is
# why it sits above the loads rather than beside the rest of the layout.

st.set_page_config(
    page_title="What a published AI register can answer",
    page_icon="▦",
    layout="wide",
)

findings = load("findings.json")
fieldset = load("fieldset.json")

lead = fieldset["lead"]
head = fieldset["headline"]

st.title("What a published AI register can and cannot answer")

st.markdown(
    "US federal agencies publish a list of the AI systems they use once a year, "
    "under a White House policy memorandum. The 2025 list holds **"
    + n(lead["entries"])
    + " entries**, of which **"
    + n(lead["high_impact"])
    + "** are marked high-impact: the list's own term for a system whose output "
    "is the main basis for a decision affecting people. It asks nine questions "
    "about how each system is checked, from whether it was tested before use to "
    "whether anyone can appeal its decisions. For **"
    + n(lead["no_oversight"])
    + " of those "
    + n(lead["high_impact"])
    + " entries all nine are blank.**"
)

st.markdown(
    "This is an audit of that list, and a field set the author would record "
    "instead. Every figure here is read from the audit's published files. "
    "[Read the full audit](" + SITE + ")."
)

st.divider()

# --- the design view, which leads ------------------------------------------
# Owner ruling of 25 September 2026: the design view leads, and the findings
# follow as the evidence it rests on.

st.header("The same form, filled twice")

st.markdown(
    "The field set holds **"
    + n(head["fields"])
    + " fields**. A published entry taken from the real register can answer **"
    + n(head["a_real_entry_can_fill"])
    + "** of them. Of the "
    + n(head["a_real_entry_cannot_fill"])
    + " it cannot, "
    + n(head["not_collected"])
    + " are questions the register does not ask at all, and "
    + n(head["asked_and_left_empty"])
    + " is asked and left empty on this entry."
)

one = fieldset["panel_one"]
two = fieldset["panel_two"]

left, right = st.columns(2)

with left:
    st.subheader("A real published entry")
    st.caption(
        one["use_case_name"]
        + ". "
        + one["agency"]
        + ". Entry "
        + one["entry_id"]
        + "."
    )
    for row in one["rows"]:
        if row["state"] == "from_source":
            st.markdown("**" + row["field"] + "**")
            st.markdown("> " + str(row["value"]))
        else:
            # The label is the data's own wording. Only its first letter is
            # changed, so that it reads as a sentence after "Empty."
            said = row.get("label") or row.get("short") or ""
            said = said[:1].upper() + said[1:] if said else ""
            st.markdown("**" + row["field"] + "**")
            st.markdown(":gray[Empty. " + said + "]")

with right:
    st.subheader("The same form, filled in")
    st.caption(two["label"])
    for row in two["rows"]:
        st.markdown("**" + row["field"] + "**")
        st.markdown("> " + str(row["value"]))

st.info(one["rule"])

st.divider()

# --- the field set ----------------------------------------------------------

st.header("The " + n(head["fields"]) + " fields, and why each one is here")

st.caption(
    "Each field exists because of something the audit found. The finding is "
    "given with it, and links to the working behind it."
)

for field in fieldset["fields"]:
    with st.expander(field["name"]):
        st.markdown("**What it records.** " + field["records"])
        st.markdown(
            "**Why it is here.** "
            + field["finding"]
            + "  [See the finding]("
            + link_for(field.get("finding_link", "index.html"))
            + ")"
        )
        st.markdown("**The 2025 US register.** " + field["us_2025"])
        st.markdown("**The Ontario register.** " + field["ontario"])
        if field.get("rests_on"):
            st.warning("**What this rests on.** " + field["rests_on"])

st.divider()

# --- the evidence -----------------------------------------------------------

st.header("What these figures rest on")

st.caption(
    "A figure appears here only if what qualifies it survives being shortened "
    "to one line that still holds. The rest are linked to rather than repeated, "
    "and are listed below."
)

columns = st.columns(len(fieldset["evidence"]))
for column, item in zip(columns, fieldset["evidence"]):
    with column:
        # Figure first, then what it is of, then what it reads, then what
        # qualifies it. The same order the site uses, so a reader who has seen
        # one recognises the other.
        figure = n(item["value"]) + item.get("suffix", "")
        if item.get("of_value") is not None:
            figure += " :gray[of " + n(item["of_value"]) + "]"
        st.markdown("### " + figure)
        st.markdown(item["reads"])
        st.caption(item["caveat"])
        st.markdown("[See the working](" + link_for(item.get("link", "index.html")) + ")")

st.subheader("Figures deliberately not shown here")

for item in fieldset["evidence_withheld"]:
    st.markdown(
        "**"
        + item["name"]
        + ".** "
        + item["why"]
        + "  [See it in full]("
        + link_for(item.get("link", "index.html"))
        + ")"
    )

st.divider()

# --- the five questions -----------------------------------------------------

st.header("The audit in five questions")

for question in findings["questions"]:
    st.markdown("**" + question["question"] + "**")
    st.markdown(question["answer"])
    st.markdown("")

st.divider()

# --- limits and sources -----------------------------------------------------

st.header("What this cannot show")

for limit in fieldset["limits"]:
    st.markdown("- " + limit)

m2 = measure(findings, "M2")
if m2.get("caveat"):
    st.markdown("**On the completeness figures.** " + m2["caveat"])

m4 = measure(findings, "M4")
if m4.get("caveat"):
    st.markdown("**On the oversight figures.** " + m4["caveat"])

st.subheader("Where the numbers come from")

based = fieldset["based_on"]
st.markdown("- " + based["sources"])
st.markdown("- Downloaded " + based["downloaded"] + ". " + based["snapshot"])
st.markdown(
    "- Every figure on this page is read from `data/derived/`, the same files "
    "the site reads. This page holds no copy of its own, so a correction "
    "cannot survive here after it has been made there."
)
st.markdown("- [The full audit](" + SITE + ")  |  [The repository](" + REPOSITORY + ")")

st.divider()

st.caption(findings["disclaimer"])
st.caption(findings["authorship"])
