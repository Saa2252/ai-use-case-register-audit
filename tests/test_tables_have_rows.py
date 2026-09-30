"""Every table the scripts fill has something to fill it with.

A reader photographed the gaps page with five tables showing their headings and
no rows, and a sentence reading "At -, - entries are flagged". That state was
caused by a cache, and the same state can be caused by a renamed key, and
nothing in this suite would have noticed either.

The rest of the suite checks the inputs. Every `data-figure` path resolves,
every data file the scripts fetch exists, every figure matches the raw file.
None of them looks at the output. A table whose source list is renamed, emptied
or moved still passes all of them and still ships as a heading with nothing
underneath, which reads as a register with values missing.

Each `<tbody id="...">` on the built site is filled by one script from one path
in the published data. This maps them and checks that each path resolves to
something with entries in it.

Three checks, so the map cannot rot:

1. Every path in the map resolves to a non-empty list or object.
2. Every tbody on the site has an entry in the map, so a new table must be
   added here before it can ship.
3. Every id in the map is still on the site, so renaming one in the markup
   fails rather than silently emptying its table.

Verified by planting the failure: emptying any mapped list in the published
JSON fails the first check and names the table, and renaming a tbody id in a
body file fails the second and third.
"""

import json

from conftest import REPO_ROOT

DOCS = REPO_ROOT / "docs"
DATA = DOCS / "data"

# tbody id -> (data file, path within it). The path is spelled as the script
# reads it. "findings" and "reusability" are keyed by measure and by id, the
# way the page's store is built, rather than by their position in the file.
TABLES = {
    "thresholds": ("findings", "M1.candidate_duplicates_not_confirmed"),
    "mismatches": ("findings", "M2.reconciliation.figures_that_do_not_match"),
    "folded": ("findings", "M2-preparation.per_category"),
    "uk-only": ("findings", "M5.asked_by_the_uk_not_by_the_federal_register"),
    "fed-only": ("findings", "M5.asked_by_the_federal_register_not_by_the_uk"),
    "bands": ("findings", "M4.bands"),
    "coverage": ("findings", "M4.oversight_field_coverage"),
    "emptylist": ("reusability", "R1.figures"),
    "tbody": ("register_table", "rows"),
}


def _stores() -> dict:
    findings = json.loads((DATA / "findings.json").read_text(encoding="utf-8"))
    reuse = json.loads((DATA / "reusability_findings.json").read_text(encoding="utf-8"))
    return {
        "findings": {f["measure"]: f for f in findings["findings"]},
        "reusability": {f["id"]: f for f in reuse["findings"]},
        "register_table": json.loads((DATA / "register_table.json").read_text(encoding="utf-8")),
    }


def _resolve(store, path):
    node = store
    for key in path.split("."):
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node


def _tbody_ids() -> set:
    import re
    found = set()
    for page in sorted(DOCS.glob("*.html")):
        found |= set(re.findall(r'<tbody id="([^"]+)"', page.read_text(encoding="utf-8")))
    return found


def test_every_table_has_rows_behind_it():
    stores = _stores()
    empty = []
    for table, (source, path) in TABLES.items():
        value = _resolve(stores[source], path)
        if value is None:
            empty.append(f"{table}: nothing at {source}.{path}")
        elif not value:
            empty.append(f"{table}: {source}.{path} is there and holds nothing")
    assert not empty, (
        "a table on the site would render its headings and no rows:\n" + "\n".join(empty)
    )


def test_every_table_on_the_site_is_in_the_map():
    unmapped = _tbody_ids() - set(TABLES)
    assert not unmapped, (
        "a table was added to the site and nothing checks that it fills: "
        + ", ".join(sorted(unmapped))
    )


def test_every_table_in_the_map_is_still_on_the_site():
    gone = set(TABLES) - _tbody_ids()
    assert not gone, (
        "the map names a table the site no longer has, so its check passes over "
        "nothing: " + ", ".join(sorted(gone))
    )
