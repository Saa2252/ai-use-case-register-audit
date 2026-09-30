"""One shape for keeping a register current, scoped to five gaps and no more.

The field set says what a register should record. It says nothing about how one
is kept, and a register nobody runs is a document rather than a control. That
sentence has been on the field set page for some time as an admission. This is
the answer to it.

**Scope, set by the owner on 30 September 2026.** Exactly the five gaps the
field set page already names, held in `src.fieldset.OPERATING_GAPS`. Not a
governance framework, not a policy, not a maturity model, not a committee
structure. Each of those is a reasonable thing to build and none of them is
this. A proposal that answers more than the gaps it was written for is a
proposal nobody asked for, and the five are what the audit produced.

**Status.** A proposal. Nothing here has been used to keep a real register, and
nothing here can be checked against a published file the way the rest of this
site can. The three audit pages state what a register contains and can be
checked against it. The field set states what one should ask. This states how
one would be kept, and it is the least checkable page on the site. It says so
at the top and again at the bottom.

Each of the five carries the same five answers, in the same order, because a
mechanism a reader cannot compare with the others is a paragraph rather than a
design: what it is, who does it, what sets it off, what it leaves behind, and
what it costs. The cost is stated for every one. A proposal with no costs in it
is a wish.
"""

from __future__ import annotations

from src.fieldset import OPERATING_GAPS

STATUS = {
    "label": "Proposal. Not tested.",
    "what_this_is": "One way to keep a register current, written against the five things "
                    "the field set does not do. It is a design, not a finding.",
    "what_this_is_not": "It has not been used to keep a register. It has not been put in "
                        "front of anyone who keeps one. Nothing on this page can be checked "
                        "against a published file, which is what the other four pages can "
                        "be checked against and what the rest of this project rests on.",
    "why_it_is_separate": "It sits on its own page so that it is never read as part of "
                          "the audit. The audit describes a file. This describes a way of "
                          "working, and the two carry different weight.",
    "scope": "Five mechanisms, one for each gap the field set names, and nothing else. "
             "No framework, no policy text, no committee, no maturity model. Each of "
             "those is a reasonable thing to build and none of them is this.",
}

# Keyed to src.fieldset.OPERATING_GAPS so the two pages cannot name different
# gaps. A key here with no gap there, or a gap there with no mechanism here,
# stops the build.
MECHANISMS = {
    "owner": {
        "mechanism": "Every entry carries one named role, not a team and not a mailbox. "
                     "The role is the one that can stop the system being used, which in "
                     "most organisations is the person who owns the process the system "
                     "sits inside rather than the person who built it.",
        "who": "The owner of the business process. The technical team is recorded "
               "separately and is not the accountable role.",
        "trigger": "Set when the entry is created. Revisited when the named role changes "
                   "hands, which is one of the five update triggers below.",
        "record": "A name and a date on the entry, and a second date when it last "
                  "changed hands. Both are readable without asking anyone.",
        "cost": "Someone has to agree to be named, and naming a person who cannot stop "
                "the system produces an owner in name only. This is the mechanism most "
                "likely to be filled in with whoever is available.",
    },
    "triggers": {
        "mechanism": "Five named events force a re-check, and one date forces one in "
                     "their absence. The five are the ones this audit found no field for: "
                     "the responsible role changes, the model or its version changes, the "
                     "data it draws on changes, what it is used for changes, or how far it "
                     "acts without a person changes.",
        "who": "The named owner confirms. Whoever makes the change raises it.",
        "trigger": "Any of the five, within a set number of working days. Otherwise a "
                   "calendar review, and the interval is set by the impact classification "
                   "rather than being one interval for everything.",
        "record": "A date of last check and which of the five set it off, both on the "
                  "entry. These are the second and third proposed fields.",
        "cost": "A trigger only works if the people making the change know the register "
                "exists. Four of the five are known to a technical team and not to a "
                "register, so this mechanism depends on a route from one to the other "
                "that does not exist by default.",
    },
    "gates": {
        "mechanism": "The entry is created before the system is bought or switched on, "
                     "not after. Two points do the work: an entry exists before money is "
                     "committed, and the entry is complete before the system is used on "
                     "real cases.",
        "who": "Whoever signs the purchase, and whoever authorises live use.",
        "trigger": "The purchase, and the move from pilot to live.",
        "record": "The entry's own creation date, earlier than the operational date the "
                  "register already asks for. Two dates in the wrong order is a visible "
                  "signal that needs no judgment to read.",
        "cost": "This is the mechanism with teeth and the one most likely to be waived "
                "under time pressure. It also reaches beyond the register into "
                "procurement, which is the only one of the five that does.",
    },
    "switched_off": {
        "mechanism": "A system that stops being used moves to a retired state on the "
                     "entry, with a date and the reason. The entry stays. It is never "
                     "deleted, because a register that empties by deletion cannot answer "
                     "what was running last year.",
        "who": "The named owner.",
        "trigger": "The system stops being used, or a calendar review finds it has not "
                   "been used since the previous one.",
        "record": "A retired state, a date, and a short reason. The published register "
                  "already has a retired stage, which is why this is the cheapest of "
                  "the five.",
        "cost": "Nobody is prompted when a system quietly stops being used, so this "
                "depends on the calendar review rather than on anyone noticing.",
    },
    "evidence": {
        "mechanism": "Every answer that asserts something points at where that thing can "
                     "be read. The nine oversight answers each carry a reference to the "
                     "document behind them rather than only a yes.",
        "who": "Whoever answers the question.",
        "trigger": "At the point the answer is given. A reference added later is a "
                   "reference nobody checked.",
        "record": "A reference on each answer. Inside an organisation this is a link. "
                  "Published outside it, it is a document name and a date, because the "
                  "link is usually behind a login.",
        "cost": "This is the mechanism that turns a yes into a claim someone can check, "
                "and for that reason it is the one people answer more slowly. Expect "
                "fewer answers and better ones.",
    },
}

# How you would know it is working. Deliberately few, and each one readable from
# the register itself rather than from asking the people who keep it, because an
# answer from the people who keep a register is the thing this whole project
# exists to look past.
SIGNALS = [
    "Entries whose creation date is earlier than their operational date, as a share "
    "of entries added since the gates were put in.",
    "Entries checked within their own interval, as a share of entries due a check.",
    "Entries in a retired state, as a count. A register that never retires anything "
    "is not being read.",
    "Oversight answers carrying a reference, as a share of oversight answers given.",
    "Entries whose named owner has changed hands with no re-check recorded.",
]

# What would show this proposal to be wrong. Written down because a design with
# no way of being wrong is not a design.
WOULD_SHOW_IT_WRONG = [
    "Someone who keeps a register says the five triggers are not the events that "
    "actually change a system, or that they are unworkable in the volumes involved.",
    "The gate at purchase turns out to be the one people route around, which would "
    "make the entry date less reliable than the operational date rather than more.",
    "Asking for a reference on every answer reduces the answers given without "
    "improving the ones that remain.",
]


def build() -> dict:
    """The page payload. Every gap gets a mechanism, and no mechanism is orphaned."""
    gaps = {g["key"]: g for g in OPERATING_GAPS}
    missing = [k for k in gaps if k not in MECHANISMS]
    orphan = [k for k in MECHANISMS if k not in gaps]
    if missing:
        raise SystemExit("gaps with no mechanism: " + ", ".join(sorted(missing)))
    if orphan:
        raise SystemExit(
            "mechanisms answering nothing the field set names: " + ", ".join(sorted(orphan)))

    return {
        "status": STATUS,
        "mechanisms": [dict(gaps[key], **MECHANISMS[key]) for key in gaps],
        "signals": SIGNALS,
        "would_show_it_wrong": WOULD_SHOW_IT_WRONG,
    }
