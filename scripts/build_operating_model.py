"""Build data/derived/operating_model.json, the fifth page's data.

Kept apart from the findings on purpose. Everything in findings.json was
counted from a published file. Nothing here was. Writing them into one file
would make the two look like the same kind of statement.

Run:  python scripts/build_operating_model.py
"""

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.disclaimer import AUTHORSHIP, DISCLAIMER  # noqa: E402
from src.operating_model import build  # noqa: E402

DERIVED = REPO_ROOT / "data" / "derived"
DOCS_DATA = REPO_ROOT / "docs" / "data"


def main() -> int:
    payload = build()
    payload["disclaimer"] = DISCLAIMER
    payload["authorship"] = AUTHORSHIP
    payload["generated"] = date.today().isoformat()
    out = json.dumps(payload, indent=2) + "\n"
    DOCS_DATA.mkdir(parents=True, exist_ok=True)
    (DERIVED / "operating_model.json").write_text(out, encoding="utf-8")
    (DOCS_DATA / "operating_model.json").write_text(out, encoding="utf-8")
    print("mechanisms: " + ", ".join(m["key"] for m in payload["mechanisms"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
