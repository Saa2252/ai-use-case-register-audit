"""Single source of truth for required published text.

Safeguard S9 requires the exact disclaimer on every page footer, at the top of
the README, and in the header of every export. Holding the wording in one place
means it cannot drift between files. Test T6 compares every published copy
against the constants below.

Only the owner may change DISCLAIMER.
"""

DISCLAIMER = (
    "This is an independent portfolio project. It uses publicly available AI use "
    "case inventories published by the US Office of Management and Budget "
    "(public domain, 17 U.S.C. §105) and the Government of Ontario (Open "
    "Government Licence – Ontario). Vendor and product names have been removed. "
    "Findings describe patterns in the published data and are not claims about any "
    "agency's conduct. This is not legal advice. Not affiliated with or endorsed by "
    "any government body."
)

# Required on export files only (M4 oversight information pack).
EXPORT_NOTICE = "Practice exercise. Not a response to any real request."

# Safeguard S11. The owner is credited for the governance design.
AUTHORSHIP = "Governance design by Sana Ahmad."

# Filled in Phase 1 by copying the statement verbatim from the Open Government
# Licence - Ontario page. Do not paraphrase it (S1).
ONTARIO_ATTRIBUTION = (
    "Contains information licensed under the Open Government Licence – Ontario."
)
ONTARIO_LICENCE_URL = "https://www.ontario.ca/page/open-government-licence-ontario"

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
