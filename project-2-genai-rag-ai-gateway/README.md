# Project 2 — Governed GenAI

Status: **code and config only. Nothing in this folder has been deployed to Databricks.**

Why: the workspace has no Unity Catalog metastore, and assigning one returned 403 (ADR-0005). Vector Search, serving endpoints, and Unity Gateway all need that metastore. Creating them anyway would have meant a workspace-local setup this portfolio is not willing to pretend is governed.

What is here:

- `src/chunking.py` and `src/guardrails.py`, unit-tested. The guardrail blocks an SSN-shaped string before any model call.
- `configs/ai-gateway-rate-limit.json` — Unity Gateway (current name) rate limits, inference table, PII block, CAN_QUERY list. Not applied.
- `configs/external-model-azure-openai.json` — template, no key. Prefers Entra ID.
- `configs/external-model-anthropic.disabled.json` and `external-model-openai.disabled.json` — `enabled: false`. Secret reference only, no secret.
- `MODEL_CARD.md` — filled, marked not deployed. No alias and no score.
- `eval/regulatory_assistant_eval.jsonl` — 25 questions. Every row has `"scored": false`.

Docs checked 2026-10-27:

- https://learn.microsoft.com/en-us/azure/databricks/ai-gateway/
- https://learn.microsoft.com/en-us/azure/databricks/unity-gateway/model-region-availability
- https://learn.microsoft.com/en-us/azure/databricks/resources/designated-services
