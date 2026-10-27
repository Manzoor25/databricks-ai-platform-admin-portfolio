"""CPU training entry point for the bank-distress classifier.

Uses only the Python standard library so CI can run it without a GPU and
without a heavy ML install. The Databricks job swaps this scoring function
for XGBoost when a cluster is available; the device parameter and the
promotion rule stay the same.

Honesty: this file has been executed on CPU. It has not been executed on CUDA.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.features import distress_label, resolve_device


def train(rows: list[dict], device: str) -> dict[str, float]:
    resolved = resolve_device(device)
    # A one-feature threshold model. Good enough to prove the promotion rule.
    # Not a claim of model quality.
    labeled = [(float(r["equity_ratio"]), distress_label(float(r["equity_ratio"]), bool(r["failed"]))) for r in rows]
    correct = sum(1 for ratio, label in labeled if (ratio < 0.06) == bool(label))
    accuracy = correct / len(labeled) if labeled else 0.0
    return {"device": resolved, "accuracy": accuracy, "rows": float(len(labeled))}


def promote(challenger: float, champion: float, approved_by: str | None) -> bool:
    """Challenger becomes champion only if it is strictly better and a human signed."""
    return bool(approved_by) and challenger > champion


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--approved-by", default="")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows = [
        {"equity_ratio": 0.02, "failed": True},
        {"equity_ratio": 0.03, "failed": False},
        {"equity_ratio": 0.11, "failed": False},
        {"equity_ratio": 0.09, "failed": False},
    ]
    metrics = train(rows, args.device)
    metrics["promoted"] = promote(metrics["accuracy"], 0.5, args.approved_by or None)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics))


if __name__ == "__main__":
    main()
