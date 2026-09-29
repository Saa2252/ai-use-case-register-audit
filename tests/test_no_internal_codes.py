"""Internal finding codes do not appear in reader-facing copy.

The findings carry short codes so that the project can refer to them. A reader
has never seen those codes and cannot look them up. They belong in the data as
identifiers and in the governance records, never in a sentence someone reads.

They appeared once, in two findings whose text explained how they differed from
others by naming them.
"""

import json
import re

from conftest import REPO_ROOT

DOCS = REPO_ROOT / "docs"
CODE = re.compile(r"\bR[1-9]\b")

# Keys that hold an identifier or a data path rather than prose. A path such as
# R3.figures.rows_with_no_usable_identifier names where a figure lives; it is
# never rendered.
IDENTIFIER_KEYS = {"id", "path"}

# Two published files contain nothing but the register's own values and the
# register's own field names. A use case is named "R1 Forest Vegetation
# Modeling" and an output is described in a format called "E2B(R2)". Those are
# the agencies' words, not this project's copy.
#
# Excluded by file rather than by key, which is the opposite of how the
# trend-word rule is scoped, and for the opposite reason: there, project prose
# and source values share a file, so a file-level exclusion would let project
# prose through. Here neither file contains a single sentence this project
# wrote, so there is nothing for a key-level rule to protect.
SOURCE_ONLY_FILES = {"register_table.json", "register_full.json"}


def prose_strings(node, key=None, path=""):
    if key in IDENTIFIER_KEYS:
        return
    if isinstance(node, dict):
        for k, v in node.items():
            yield from prose_strings(v, k, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from prose_strings(v, key, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


def test_no_internal_codes_in_published_prose():
    problems = []
    for data_file in sorted((DOCS / "data").glob("*.json")):
        if data_file.name in SOURCE_ONLY_FILES:
            continue
        try:
            payload = json.loads(data_file.read_text())
        except ValueError:
            continue
        for path, text in prose_strings(payload):
            if CODE.search(text):
                problems.append(f"{data_file.name} :: {path} :: {CODE.search(text).group(0)}")
    assert not problems, (
        "internal finding codes in reader-facing copy:\n" + "\n".join(problems))


def test_no_internal_codes_in_visible_page_text():
    """Codes may appear in data-figure attributes. They may not appear in text."""
    problems = []
    for page in sorted(DOCS.glob("*.html")):
        text = page.read_text()
        text = re.sub(r'data-figure="[^"]*"', " ", text)   # attributes are not copy
        text = re.sub(r"<[^>]+>", " ", text)               # what is left is what a reader sees
        for match in CODE.finditer(text):
            problems.append(f"{page.name}: {match.group(0)}")
    assert not problems, "internal finding codes visible on a page:\n" + "\n".join(problems)
