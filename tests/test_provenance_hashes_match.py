"""Every hash written in the provenance document is the hash of the file.

`governance/data-provenance.md` is the published record. It is what a reader
checks the project against, and it is typed by hand. T7 compares the files on
disk against the machine manifest, and nothing compared the published document
against either.

That gap produced a real fault. A hash was recorded from a shortened display of
it and the tail was wrong. The file was right, the manifest was right, and the
document a reader would check stated a hash that matched nothing.

Skips when the manifest is absent, in the same way as T1 and T7, because raw
data is never committed.

Verified by planting the failure: changing one character of any hash in the
document makes this fail and names the file.
"""

import json
import re
import sys

import pytest

from conftest import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT))

MANIFEST = REPO_ROOT / "data" / "raw" / "manifest.json"
DOCUMENT = REPO_ROOT / "governance" / "data-provenance.md"


def _manifest() -> dict:
    if not MANIFEST.exists():
        pytest.skip("raw manifest not present: run scripts/acquire.py first")
    return {d["local_name"]: d for d in json.loads(MANIFEST.read_text(encoding="utf-8"))}


def test_every_hash_in_the_document_matches_the_file_it_names():
    manifest = _manifest()
    text = DOCUMENT.read_text(encoding="utf-8")
    wrong = []
    for row in re.finditer(r"\|\s*`([^`]+)`\s*\|[^|]*\|[^|]*\|\s*`([0-9a-f]{64})`\s*\|", text):
        name, stated = row.group(1), row.group(2)
        entry = manifest.get(name)
        if entry is None:
            continue
        if entry["sha256"] != stated:
            wrong.append(f"{name}\n    document: {stated}\n    file:     {entry['sha256']}")
    assert not wrong, (
        "the published provenance record states a hash that is not the file's:\n"
        + "\n".join(wrong)
    )


def test_every_downloaded_file_appears_in_the_document():
    manifest = _manifest()
    text = DOCUMENT.read_text(encoding="utf-8")
    missing = [name for name in manifest if f"`{name}`" not in text]
    assert not missing, (
        "a source was downloaded and the published record does not name it: "
        + ", ".join(sorted(missing))
    )
