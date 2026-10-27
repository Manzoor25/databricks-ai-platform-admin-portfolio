"""Feature logic for the bank-distress classifier.

Runs on CPU. The same function is what a Feature Engineering table would store.
`device` is accepted so the training job can pass cpu or cuda without a rewrite.
This module does not import torch. XGBoost/LightGBM are optional; the pure
function is the part that must be testable in CI.
"""

from __future__ import annotations


def capital_buffer(equity_ratio: float, minimum_required: float = 0.08) -> float:
    return equity_ratio - minimum_required


def distress_label(equity_ratio: float, failed: bool) -> int:
    """1 if the bank failed or its equity ratio is under 4 percent."""
    if failed or equity_ratio < 0.04:
        return 1
    return 0


def resolve_device(requested: str) -> str:
    """Honor cuda only when the caller has already confirmed a GPU.

    This function does not probe hardware. The job passes the result of that
    probe. Default is cpu. Never claim cuda was used unless the job log says so.
    """
    if requested not in {"cpu", "cuda"}:
        raise ValueError("device must be cpu or cuda")
    return requested
