"""Single source of truth for required published text.

Safeguard S9 requires the exact disclaimer on every page footer, at the top of
the README, and in the header of every export. Holding the wording in one place
means it cannot drift between files. Test T6 compares every published copy
against the constants below.

Only the owner may change DISCLAIMER.
"""

# Changed by the owner on 2026-09-30, the only change since Phase 0. The UK
# Government's recording standard became a source on 2026-09-30 and the text
# named only the two earlier ones. The standard is a template rather than an
# inventory, so it is named as its own clause rather than added to the list of
# inventories.
DISCLAIMER = (
    "This is an independent portfolio project. It uses publicly available AI use "
    "case inventories published by the US Office of Management and Budget "
    "(public domain, 17 U.S.C. §105) and the Government of Ontario (Open "
    "Government Licence – Ontario), and the UK Government's Algorithmic "
    "Transparency Recording Standard template (© Crown copyright, Open Government "
    "Licence v3.0). Vendor and product names have been removed. "
    "Findings describe patterns in the published data and are not claims about any "
    "agency's conduct. This is not legal advice. Not affiliated with or endorsed by "
    "any government body."
)

# Required on export files only (M4 oversight information pack).
EXPORT_NOTICE = "Practice exercise. Not a response to any real request."

# Safeguard S11. The owner is credited for the governance design.
AUTHORSHIP = "Governance design by Sana Ahmad."

# Who this is by and why, at the top of the landing page. Added 30 September
# 2026 at the owner's request: the only mention of them was the footer credit,
# which a reader reaches last if at all.
#
# **What this deliberately does not say.** S11 forbids claiming or describing
# who wrote the code, and `tests/test_authorship_claims.py` looks for the
# likely phrasings, "built by" among them. This attributes the project and
# states its purpose. It says nothing about who wrote any of it.
#
# It also asserts nothing about the owner beyond their name. Anything about
# their background is theirs to write, not this project's to infer, and a
# portfolio that invents a line about the person is worse than one that says
# nothing.
ABOUT_LEAD = "A portfolio project by Sana Ahmad."
ABOUT = ("It asks what an AI use case register should record, and answers it by auditing a "
         "real one rather than reasoning from first principles. Every figure, decision rule "
         "and safeguard is open, including the ones this project got wrong and corrected.")
ABOUT_LINK_TEXT = "The working, in full"

# Filled in Phase 1 by copying the statement verbatim from the Open Government
# Licence - Ontario page. Do not paraphrase it (S1).
ONTARIO_ATTRIBUTION = (
    "Contains information licensed under the Open Government Licence – Ontario."
)
ONTARIO_LICENCE_URL = "https://www.ontario.ca/page/open-government-licence-ontario"

# The Open Government Licence v3.0 sets this wording for use where the
# Information Provider gives no attribution statement of its own. Copied
# verbatim from the licence at nationalarchives.gov.uk on 2026-09-30. Do not
# paraphrase it (S1).
UK_ATTRIBUTION = (
    "Contains public sector information licensed under the Open Government Licence v3.0."
)
UK_LICENCE_URL = "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"

# The repository the project is published from. Empty until the owner creates it
# and sends the address; every place that shows the link reads it from here, and
# nothing renders a link while it is empty.
#
# The owner approved two exact-string exemptions for this one value on
# 2026-09-30, recorded with their reasons in governance/safeguards.md:
#   T2 (no vendor or product terms) would otherwise match the hosting provider's
#   name inside the address.
#   T5 (no typed numbers in published pages) would otherwise match the digits
#   inside the account name.
# Both exemptions cover this exact string and nothing else. They are written as
# a comparison against REPOSITORY_URL rather than a pattern, so widening one
# means changing this value, which is a stop-and-ask.
REPOSITORY_URL = "https://github.com/Saa2252/ai-use-case-register-audit"

# Where the site is published. Held here because a second surface now points at
# it, and two places stating an address is two addresses that can disagree.
# The README states it from here, and so does the Streamlit application.
SITE_URL = "https://saa2252.github.io/ai-use-case-register-audit/"
