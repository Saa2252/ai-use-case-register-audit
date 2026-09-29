"""A fact this site states on more than one page comes from one place.

A fact written out independently on two pages is two facts that can disagree.
This project has been bitten twice. An emptiness rule implemented in two places
had drifted, 28 values against 21, before anyone looked. A sentence asserting
who has to publish a register was corrected on the landing page and survived
unchanged on the register page, because each page stated it on its own.

src/statements.py holds each shared statement once. Page bodies carry a
`{{key}}` token and scripts/build_site.py substitutes it. This test fails if a
body writes one of those statements out instead of using its token.

Verified by planting the failure: pasting any statement's text back into a body
file makes this fail and names the file and the key.
"""

import sys

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))
from src.statements import STATEMENTS  # noqa: E402

BODIES = REPO_ROOT / "scripts" / "bodies"
DOCS = REPO_ROOT / "docs"


def _normalise(text: str) -> str:
    return " ".join(text.replace("’", "'").split()).lower()


def test_no_body_writes_out_a_shared_statement():
    written_out = []
    for body in sorted(BODIES.glob("*.html")):
        text = _normalise(body.read_text())
        for key, statement in STATEMENTS.items():
            if _normalise(statement) in text:
                written_out.append(
                    f"{body.name} writes out the statement '{key}' instead of using "
                    f"{{{{{key}}}}}"
                )
    assert not written_out, (
        "a fact is stated independently instead of coming from src/statements.py:\n"
        + "\n".join(written_out)
    )


def test_every_token_resolves():
    """A token nobody substitutes would ship as literal braces."""
    leftovers = []
    for page in sorted(DOCS.glob("*.html")):
        text = page.read_text()
        if "{{" in text:
            start = text.index("{{")
            leftovers.append(f"{page.name}: {text[start:start + 40]!r}")
    assert not leftovers, "an unsubstituted token reached a published page:\n" + "\n".join(leftovers)


def test_shared_statements_reach_the_pages_they_belong_on():
    """Substitution actually happened, rather than silently producing nothing."""
    pages = {p.name: _normalise(p.read_text()) for p in DOCS.glob("*.html")}
    expected = {
        "publication_duty": ["index.html", "register.html"],
        "high_impact_meaning": ["register.html", "obligations.html"],
        "filled_field": ["register.html"],
        "reached_the_file": ["register.html"],
    }
    missing = []
    for key, wanted in expected.items():
        statement = _normalise(STATEMENTS[key])
        for page in wanted:
            if statement not in pages.get(page, ""):
                missing.append(f"{page} should carry the statement '{key}' and does not")
    assert not missing, "a shared statement did not reach its page:\n" + "\n".join(missing)
