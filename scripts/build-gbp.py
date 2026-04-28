"""Build taxonomy/gbp-categories.json from a PlePer Tools TSV export.

Google Business Profile categories evolve roughly monthly. This script
takes the TSV exported from PlePer Tools (open the tool with EN/US
selected, copy the table, paste into a .tsv file) and produces the
canonical JSON shape used by the protocol.

Usage:
    # 1. Save the TSV (e.g. via PlePer's copy-to-clipboard) at:
    #      taxonomy/sources/gbp-pleper-<YYYY-MM-DD>.tsv
    #    Format: GCID<TAB>Category, with a header row.
    #
    # 2. Run the build (paths and output overridable via env vars):
    GBP_TSV=taxonomy/sources/gbp-pleper-2026-04-28.tsv \\
    GBP_SNAPSHOT=2026-04-28 \\
        python3 scripts/build-gbp.py

The output is a bare JSON array of {gcid, name, parent_naics_code,
parent_path} objects. parent_naics_code and parent_path are null on
every entry for now — no authoritative GBP→NAICS mapping exists, and
PlePer's export doesn't carry breadcrumb paths. See
taxonomy/gbp-categories.README.md.

No external dependencies; standard library only.
"""
import csv
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TSV_PATH = Path(os.environ.get(
    "GBP_TSV", REPO_ROOT / "taxonomy" / "sources" / "gbp-pleper-2026-04-28.tsv"
))
OUT_PATH = Path(os.environ.get(
    "GBP_OUT", REPO_ROOT / "taxonomy" / "gbp-categories.json"
))
SNAPSHOT_DATE = os.environ.get("GBP_SNAPSHOT", "2026-04-28")


def main() -> int:
    if not TSV_PATH.exists():
        sys.stderr.write(f"input TSV not found: {TSV_PATH}\n")
        return 2

    entries: list[dict] = []
    seen_gcids: set[str] = set()
    duplicates: list[str] = []
    skipped_blanks = 0

    with TSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader, None)
        if not header or [c.strip().lower() for c in header[:2]] != ["gcid", "category"]:
            sys.stderr.write(
                f"unexpected header in {TSV_PATH}: {header!r}; "
                "expected ['GCID', 'Category']\n"
            )
            return 2

        for row in reader:
            if len(row) < 2:
                skipped_blanks += 1
                continue
            gcid = row[0].strip()
            name = row[1].strip()
            if not gcid or not name:
                skipped_blanks += 1
                continue
            if gcid in seen_gcids:
                duplicates.append(gcid)
                continue
            seen_gcids.add(gcid)
            entries.append({
                "gcid": gcid,
                "name": name,
                "parent_naics_code": None,
                "parent_path": None,
            })

    entries.sort(key=lambda e: e["gcid"])

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"snapshot:        {SNAPSHOT_DATE}")
    print(f"input:           {TSV_PATH.relative_to(REPO_ROOT)}")
    print(f"output:          {OUT_PATH.relative_to(REPO_ROOT)}")
    print(f"entries written: {len(entries):,}")
    print(f"duplicates:      {len(duplicates)}"
          + (f" (first 5: {duplicates[:5]})" if duplicates else ""))
    print(f"blank rows:      {skipped_blanks}")
    print(f"output bytes:    {OUT_PATH.stat().st_size:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
