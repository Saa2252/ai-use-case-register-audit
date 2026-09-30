"""Download every source and rebuild the provenance manifest.

Phase 1, as a script. It was done by hand, which left two holes.

The manifest listed twelve files. The UK template was not among them, so T7
had not checked it since it became a source on 30 September 2026. A file
outside the manifest can be edited and no test notices, which is the whole
point of S7.

And nothing in the repository declared the download addresses. The notebook
said Phase 1 was not implemented. Anyone following the README could not have
reproduced the raw files at all.

Every source the project reads is declared below, with its address and what it
is for. Running this downloads anything absent, re-hashes everything present,
and writes `data/raw/manifest.json`, which T7 verifies. A file already on disk
is never overwritten (S7), so a re-run does not disturb what was verified.

Run:  python scripts/acquire.py
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.provenance import fetch, write_manifest  # noqa: E402

GITHUB_2025 = ("https://raw.githubusercontent.com/ombegov/"
               "2025-Federal-Agency-AI-Use-Case-Inventory/main/")
GITHUB_2024 = ("https://raw.githubusercontent.com/ombegov/"
               "2024-Federal-AI-Use-Case-Inventory/main/")
ONTARIO = ("https://data.ontario.ca/dataset/29c77a6b-22d3-434e-94d5-51b25d8d8cc0/"
           "resource/")

# The European Union's own repository serves one document in several formats
# and languages from a single address and picks between them by these headers.
# EUR-Lex itself answers a scripted request with an empty body.
EU_HEADERS = {"Accept": "application/xhtml+xml", "Accept-Language": "eng"}

# local name, url, source, note, headers
SOURCES = [
    ("omb2025_individually_reported.csv", GITHUB_2025 + "Data/2025_individually_reported_AI_use_cases.csv",
     "OMB 2025", "The core dataset. One row per declared use case.", None),
    ("omb2025_consolidated_cots.csv", GITHUB_2025 + "Data/2025_consolidated_COTS_AI_use_cases.csv",
     "OMB 2025", "The second reporting route. Counts something different and is never summed with the first.", None),
    ("omb2025_data_dictionary.json", GITHUB_2025 + "Validation/data_dictionary.json",
     "OMB 2025", "Field definitions, allowed answers and the Required clause this project reads for every denominator.", None),
    ("omb2025_data_dictionary.md", GITHUB_2025 + "Validation/data_dictionary.md",
     "OMB 2025", "The same dictionary as prose.", None),
    ("omb2025_README_datasets.md", GITHUB_2025 + "Data/README_datasets.md",
     "OMB 2025", "What each published file contains.", None),
    ("omb2025_README.md", GITHUB_2025 + "README.md",
     "OMB 2025", "Published totals, inclusion rules and the submission schedule this project reconciles against.", None),

    ("omb2024_inventory_v1.csv", GITHUB_2024 + "data/2024_consolidated_ai_inventory_raw.csv",
     "OMB 2024", "Schema reference only. Its rows are not read.", None),
    ("omb2024_inventory_v2.csv", GITHUB_2024 + "data/2024_consolidated_ai_inventory_raw_v2.csv",
     "OMB 2024", "The second of two files with near-identical names, recorded because the pair is a counting trap.", None),
    ("omb2024_data_dictionary.yaml", GITHUB_2024 + "validation/data_dictionary.yaml",
     "OMB 2024", "Field definitions for the earlier year.", None),
    ("omb2024_README.md", GITHUB_2024 + "README.md",
     "OMB 2024", "Inclusion rules for the earlier year.", None),

    ("ontario_ai_use_cases_en.csv", ONTARIO + "70c67d83-ded3-45e5-adcc-8335db98e6b1/download/4._ai_use_cases_in_the_ops.csv",
     "Ontario", "Kept for one observation: no supplier is named in any published field.", None),
    ("ontario_ai_use_cases_fr.csv", ONTARIO + "b8778f78-f1dc-4f95-9bd1-2420bb4cbc11/download/4._cas_dutilisation_de_lia_dans_la_fpo_1.csv",
     "Ontario", "French translation. Not analysed. Recorded so the register is not read as twice its size.", None),

    ("uk_atrs_template_v4.xlsx", "https://assets.publishing.service.gov.uk/media/681b8f20e26cd2f713d8705d/ATRS_V4.0__FINAL.xlsx",
     "UK ATRS", "The comparator. The published field template, v4.0. No UK records are downloaded.", None),

    ("omb_m_25_21.pdf", "https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-21-Accelerating-Federal-Use-of-AI-through-Innovation-Governance-and-Public-Trust.pdf",
     "OMB memorandum", "The memorandum the 2025 dictionary cites for high-impact AI, and the only place the dates behind the oversight fields are written down.", None),

    ("eu_ai_act_consolidated_20260727.xhtml", "http://publications.europa.eu/resource/celex/02024R1689-20260727",
     "EU AI Act", "Regulation (EU) 2024/1689, consolidated text as at 27 July 2026, CELEX 02024R1689-20260727. Read for Article 49, Article 71 and Annex VIII.", EU_HEADERS),

    ("nist_ai_rmf_100_1.pdf", "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
     "NIST AI RMF", "AI Risk Management Framework 1.0, NIST AI 100-1. Read for the GOVERN subcategories on keeping an inventory.", None),
]

# Built by earlier phases from the sources above, not downloaded. Listed so the
# manifest covers every file in data/raw/ and nothing sits outside T7 unnoticed.
BUILT_LOCALLY = {
    "vendor_terms.txt", "vendor_terms_candidate_C.txt", "vendor_terms_excluded.txt",
    "vendor_terms_ordinary_word_brands.txt", "vendor_terms_removed_as_nonvendor.txt",
    "scrub_review_terms.md", "scrub_sample_20.md", "scrub_stats.json",
    "term_matching.json", "field_inventory.json", "completeness_2025.json",
    "empty_value_rule.json", "c_active_terms.json", "c_dropped_active.json",
    "c_true_gaps.json", "manifest.json", ".gitkeep",
}


def main() -> int:
    downloads = []
    for local_name, url, source, note, headers in SOURCES:
        before = (REPO_ROOT / "data" / "raw" / local_name).exists()
        downloads.append(fetch(url, local_name, source, note=note, headers=headers))
        print(f"{'have' if before else 'got '}  {local_name}")
    path = write_manifest(downloads)

    present = {p.name for p in (REPO_ROOT / "data" / "raw").iterdir() if p.is_file()}
    declared = {d.local_name for d in downloads} | BUILT_LOCALLY
    stray = sorted(present - declared)
    if stray:
        print("\nIn data/raw and declared nowhere:")
        for name in stray:
            print("  " + name)
    print(f"\nmanifest: {path.relative_to(REPO_ROOT)}  sources: {len(downloads)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
