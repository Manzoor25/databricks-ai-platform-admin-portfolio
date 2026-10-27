# Project 3 — Genie, classic ML governance, AI feature controls

Status: **training entry point ran on CPU. Genie space, serving endpoint, and feature store were not created** (no metastore, ADR-0005).

Verified:

- `python -m src.train --device cpu --approved-by mamoh` wrote `evidence/cpu-train.json`.
- Promotion requires a strictly better metric and a non-empty `approved_by`.
- `resolve_device` accepts `cpu` or `cuda` and rejects anything else. Passing `cuda` here would still not mean a GPU was used. No CUDA run exists.

Not verified, and not claimed:

- Genie space "FDIC Bank Health Explorer"
- A serverless SQL warehouse
- Feature Engineering in Unity Catalog
- Model serving, inference table, Lakehouse Monitoring
- AI Runtime / serverless GPU. Docs say it is available in the United States geo (checked 2026-10-26). This session did not attach a notebook to it.

GPU policy and the enablement runbook live in `infra/compute.tf` and `docs/runbooks/enable-gpu-compute.md`.
