"""Download public FDIC BankFind pages to local JSONL for the bronze load.

This runs on the laptop. It does not need a metastore. The Databricks job
reads the same endpoints directly when Unity Catalog is available.

Usage:
  python -m src.ingest_fdic --out ../../evidence/fdic
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.fdic_client import FdicClient
from src.synthetic_pii import generate_complaints

FAILURE_FIELDS = ["NAME", "CERT", "FAILDATE", "CITY", "STATE", "QBFASSET"]
INSTITUTION_FIELDS = ["NAME", "CERT", "STALP", "CITY", "ASSET", "ACTIVE", "REPDTE"]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--institution-limit", type=int, default=200)
    args = parser.parse_args()

    client = FdicClient()
    failures = client.iter_records("failures", FAILURE_FIELDS, sort_by="FAILDATE", page_size=200)
    institutions = client.iter_records(
        "institutions",
        INSTITUTION_FIELDS,
        filters="ACTIVE:1",
        sort_by="ASSET",
        page_size=200,
        max_records=args.institution_limit,
    )
    complaints = generate_complaints(50, seed=42)
    write_jsonl(args.out / "failures.jsonl", failures)
    write_jsonl(args.out / "institutions.jsonl", institutions)
    write_jsonl(args.out / "synthetic_complaints.jsonl", complaints)
    print(
        json.dumps(
            {
                "failures": len(failures),
                "institutions": len(institutions),
                "synthetic_complaints": len(complaints),
                "out": str(args.out),
            }
        )
    )


if __name__ == "__main__":
    main()
