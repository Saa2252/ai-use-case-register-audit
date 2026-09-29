"""Every figure on the landing page's evidence strip still matches its finding.

The strip's numbers are resolved when the site is built rather than fetched in
the browser, so the landing page does not have to download every finding on the
site to read five numbers out of them. That saves the reader two files, and it
introduces one risk: the published figure could sit still while the finding it
came from moves. This test closes that.

Verified by planting the failure: changing one resolved value in
docs/data/fieldset.json by one makes this test fail and naming the path.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DERIVED = REPO_ROOT / "data" / "derived"
DOCS_DATA = REPO_ROOT / "docs" / "data"


def _store():
    store = {}
    for name, key in (("findings.json", "measure"), ("reusability_findings.json", "id")):
        payload = json.loads((DERIVED / name).read_text())
        for finding in payload.get("findings", []):
            store[finding[key]] = finding
    return store


def _resolve(store, path):
    node = store
    for part in path.split("."):
        node = node.get(part) if isinstance(node, dict) else None
    return node


def test_evidence_figures_match_their_findings():
    store = _store()
    drift = []
    for published in (DERIVED / "fieldset.json", DOCS_DATA / "fieldset.json"):
        strip = json.loads(published.read_text())["evidence"]
        assert strip, f"{published.name} carries no evidence strip"
        for item in strip:
            expected = _resolve(store, item["path"])
            assert expected is not None, f"{item['path']} is not in the findings"
            if item["value"] != expected:
                drift.append(
                    f"{published.parent.name}/{published.name}: {item['path']} "
                    f"is published as {item['value']} and the finding says {expected}"
                )
            if item.get("of"):
                expected_of = _resolve(store, item["of"])
                if item.get("of_value") != expected_of:
                    drift.append(
                        f"{published.parent.name}/{published.name}: {item['of']} "
                        f"is published as {item.get('of_value')} and the finding "
                        f"says {expected_of}"
                    )
    assert not drift, "evidence strip has drifted from the findings:\n" + "\n".join(drift)


def test_landing_page_does_not_fetch_the_findings_files():
    """The saving only holds while the page stops asking for them."""
    script = (REPO_ROOT / "docs" / "assets" / "proposal.js").read_text()
    for name in ("findings.json", "reusability_findings.json"):
        assert name not in script, (
            f"proposal.js fetches {name} again. The landing page's figures are "
            "resolved at build time so it does not have to."
        )
