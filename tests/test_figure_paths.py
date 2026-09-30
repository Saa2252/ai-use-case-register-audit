"""Every data-figure path on the site resolves in the published JSON.

Enforces: S5 in practice. T5 proves no number is written into the markup; this
proves the markup asks for numbers that actually exist. Without it a typo in a
path renders as "unavailable" on the live page and no test notices.
"""

import json
import re

from conftest import REPO_ROOT

DOCS = REPO_ROOT / "docs"


def store() -> dict:
    """What the findings pages fill their figures from."""
    data = {}
    findings = json.loads((DOCS / "data" / "findings.json").read_text())
    for f in findings["findings"]:
        data[f["measure"]] = f
    data["corrections"] = findings.get("corrections", {})
    reuse = json.loads((DOCS / "data" / "reusability_findings.json").read_text())
    for f in reuse["findings"]:
        data[f["id"]] = f
    return data


def store_for(page) -> dict:
    """Each page resolves its figures against the data that page loads.

    Page four loads a different file from the findings pages. Checking every
    page against one store would either pass paths that cannot resolve on the
    page that uses them, or reject paths that resolve perfectly well.
    """
    text = page.read_text()
    if "assets/proposal.js" in text:
        return json.loads((DOCS / "data" / "fieldset.json").read_text())
    return store()


def resolve(data, path):
    node = data
    for key in path.split("."):
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node


def test_every_figure_path_resolves():
    missing = []
    for page in sorted(DOCS.glob("*.html")):
        data = store_for(page)
        for path in re.findall(r'data-figure="([^"]+)"', page.read_text()):
            if resolve(data, path) is None:
                missing.append(f"{page.name}: {path}")
    assert not missing, "data-figure paths that resolve to nothing:\n" + "\n".join(missing)


# Two scripts fill data-figure placeholders, from two different data files. A
# page loads exactly one of them: loading both leaves whichever finishes second
# writing over the first, and the loser's elements read "unavailable".
FIGURE_FILLERS = ["assets/figures.js", "assets/proposal.js"]


def test_every_page_loads_exactly_one_figure_script():
    problems = []
    for page in sorted(DOCS.glob("*.html")):
        text = page.read_text()
        loaded = [s for s in FIGURE_FILLERS if s in text]
        if len(loaded) != 1:
            problems.append(f"{page.name}: loads {loaded or 'none'}")
    assert not problems, (
        "pages that do not load exactly one script to fill their figures:\n" + "\n".join(problems))


def test_every_data_file_the_scripts_request_exists():
    """The page can only load data that is actually published beside it.

    The path test above proves the markup asks for figures that exist inside the
    JSON. This proves the JSON itself is where the page will look for it. Neither
    can prove the browser succeeded in fetching it, which is why the page carries
    a visible message when the load fails.
    """
    import re
    requested = set()
    for script in sorted((DOCS / "assets").glob("*.js")):
        text = script.read_text()
        requested |= set(re.findall(r'fetch\("([^"?]+)"', text))
        # Data files are requested through a helper that adds a cache stamp.
        requested |= {"data/" + n for n in re.findall(r'dataUrl\("([^"]+)"\)', text)}
    missing = [r for r in sorted(requested) if not (DOCS / r).exists()]
    assert not missing, f"scripts fetch files that are not published: {missing}"


def test_pages_announce_a_total_load_failure():
    """A page whose data did not load must say so, not show every figure as unavailable."""
    js = (DOCS / "assets" / "figures.js").read_text()
    assert "loadfail" in js, "figures.js has no visible message for a total load failure"
    assert "The data did not load" in js, "the load-failure message does not say the data did not load"
    css = (DOCS / "assets" / "style.css").read_text()
    assert ".loadfail" in css, "the load-failure message has no styling, so it may render invisibly"


def test_no_script_restates_the_emptiness_rule():
    """The rule for what counts as an empty value lives in one place.

    It was implemented twice once already. The rule file held twenty-eight
    values and the copy in the page script held twenty-one, so seven values
    counted as empty in every published figure while the page showed them as
    raw text. Nothing caught it until one entry was checked by hand.

    Detection works on proximity rather than on matching a list literal,
    because the values themselves contain brackets and a bracket-matching
    pattern cannot span them. An earlier version of this test could not, and
    passed against a restatement planted to check it.
    """
    import re

    TELLS = {"[]", "n/a", "tbd", "not available", "unknown", "none", "nan", "pending"}
    WINDOW = 200

    offenders = []
    for script in sorted((DOCS / "assets").glob("*.js")):
        text = script.read_text()
        hits = [m.start() for m in re.finditer(r'"([^"]*)"', text)
                if m.group(1).strip().lower() in TELLS]
        for i, position in enumerate(hits):
            near = [h for h in hits[i:] if h - position <= WINDOW]
            if len(near) >= 3:
                line = text[:position].count("\n") + 1
                offenders.append(f"{script.name}:{line} restates the emptiness rule")
                break
    assert not offenders, (
        "the emptiness rule is restated in a script instead of fetched:\n" + "\n".join(offenders))
