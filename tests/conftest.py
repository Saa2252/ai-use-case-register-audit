"""Shared fixtures for the safeguard tests.

Every test in this folder enforces one of the safeguards S1 to S12 listed in
governance/safeguards.md. A test is never deleted or weakened to make it pass
(the owner's brief, section 6).
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

NOT_IMPLEMENTED = "Stub created in Phase 0. Implemented in Phase 3."


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def derived_dir(repo_root: Path) -> Path:
    return repo_root / "data" / "derived"


@pytest.fixture
def raw_dir(repo_root: Path) -> Path:
    return repo_root / "data" / "raw"


@pytest.fixture
def docs_dir(repo_root: Path) -> Path:
    return repo_root / "docs"


@pytest.fixture
def html_pages(docs_dir: Path) -> list[Path]:
    return sorted(docs_dir.glob("*.html"))
