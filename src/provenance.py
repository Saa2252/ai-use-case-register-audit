"""Download sources, record provenance, verify hashes.

Phase 1. Enforces S1 (source attribution), S6 (reconcile to published totals)
and S7 (raw data untouched).

Nothing here edits a downloaded file. Files land in data/raw/, are hashed, and
are read only. All transformation happens later, on copies written to
data/derived/.
"""

from __future__ import annotations

import hashlib
import json
import urllib.request
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW = REPO_ROOT / "data" / "raw"

USER_AGENT = "ai-use-case-register-audit/0.1 (portfolio project; provenance capture)"


@dataclass
class Download:
    """One downloaded file and everything needed to prove where it came from."""

    local_name: str
    source: str
    url: str
    downloaded: str
    sha256: str
    bytes: int
    note: str = ""


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, local_name: str, source: str, note: str = "",
          headers: dict[str, str] | None = None) -> Download:
    """Download one file into data/raw/ and record its provenance.

    Never overwrites silently: if the file exists, it is hashed and returned as
    is, so a re-run does not disturb what was already verified (S7).

    `headers` adds request headers. The European Union's official repository
    serves a document in several formats and languages from one address and
    chooses between them by the Accept and Accept-Language headers, so a
    source there cannot be fetched without them. An
    empty download is treated as a failure rather than written, because a
    server that answers a script with an empty body has refused it, and a
    zero-byte file would otherwise be hashed and recorded as if it were the
    source.
    """
    RAW.mkdir(parents=True, exist_ok=True)
    dest = RAW / local_name

    if not dest.exists():
        sent = {"User-Agent": USER_AGENT}
        sent.update(headers or {})
        req = urllib.request.Request(url, headers=sent)
        with urllib.request.urlopen(req, timeout=180) as r:
            body = r.read()
        if not body:
            raise RuntimeError(
                f"{url} returned an empty body. The host answered the request and sent "
                "nothing, which is a refusal, not a file.")
        dest.write_bytes(body)

    return Download(
        local_name=local_name,
        source=source,
        url=url,
        downloaded=date.today().isoformat(),
        sha256=sha256_of(dest),
        bytes=dest.stat().st_size,
        note=note,
    )


def write_manifest(downloads: list[Download], path: Path | None = None) -> Path:
    """Write the machine-readable provenance manifest.

    Lives in data/raw/ so it is never committed. The human-readable record in
    governance/data-provenance.md is what the repository publishes.
    """
    path = path or (RAW / "manifest.json")
    path.write_text(json.dumps([asdict(d) for d in downloads], indent=2) + "\n")
    return path


def verify(downloads: list[Download]) -> list[str]:
    """Re-hash every file and report any that no longer match. Used by test T7."""
    problems = []
    for d in downloads:
        p = RAW / d.local_name
        if not p.exists():
            problems.append(f"missing: {d.local_name}")
        elif sha256_of(p) != d.sha256:
            problems.append(f"hash changed: {d.local_name}")
    return problems
