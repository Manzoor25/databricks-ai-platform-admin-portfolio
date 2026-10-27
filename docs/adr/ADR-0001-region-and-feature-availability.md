# ADR-0001: Region and feature availability

- Status: Accepted
- Date: 2026-10-27
- Docs checked: 2026-10-27

## Context

The lab must run Foundation Model APIs (pay-per-token), custom model serving, Vector Search / AI Search, serverless SQL, and (if available) serverless GPU compute. GPU VM quota in the subscription is not a blocker: classic GPU node families that matter (T4/A100/H100) have limit 0, and this ADR does not request quota.

## Decision

Deploy the Premium workspace in **East US (`eastus`)**.

Verified on 2026-10-27 from:

- [Features with limited regional availability](https://learn.microsoft.com/en-us/azure/databricks/resources/feature-region-support) (page date 2026-10-21). The `eastus` row is marked supported for serverless compute (notebooks, jobs, pipelines, SQL warehouses), AI Search, `ai_parse_document` v2, other AI functions, custom model serving (CPU), external models, Foundation Model APIs pay-per-token, and Unity Gateway.
- [Model availability by region](https://learn.microsoft.com/en-us/azure/databricks/unity-gateway/model-region-availability) (page date 2026-10-26). Pay-per-token is supported in core US regions; exact model names are read from the workspace at deploy time because the catalog changes weekly.
- [Databricks Designated Services](https://learn.microsoft.com/en-us/azure/databricks/resources/designated-services) (page date 2026-10-26). United States geo lists AI Runtime, pay-per-token Foundation Model APIs, AI Search reranker, and built-in LLM judges as **Available** (not cross-geo). East US is in the United States geo.
- [AI Runtime overview](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/ai-runtime/overview) (page date 2026-10-21). AI Runtime is Databricks-managed serverless GPU (A10/H100). It does not consume this subscription's VM quota.

## Naming changes recorded at doc check

| Brief name | Current product name (2026-10-27) | How this repo handles it |
| --- | --- | --- |
| AI Gateway | Unity Gateway | Govern endpoints through Unity Gateway; keep the admin concept (rate limits, inference tables, guardrails, fallback) in docs |
| Mosaic AI Vector Search | AI Search / Lakehouse Real-Time | Create an AI Search endpoint and a Delta Sync index if the API accepts it; otherwise document the blocker |
| Delta Live Tables | Lakeflow Declarative Pipelines | Bundle pipeline uses the current Lakeflow/SDP definition |
| Databricks Asset Bundles | Declarative Automation Bundles (docs); CLI still `databricks bundle`) | Use `databricks.yml` and `databricks bundle validate` |
| Databricks Assistant | Databricks Assistant + Genie Code | Capture workspace AI toggle state via API |

## Consequences

- Cross-geo processing stays **off**. US geo already covers the features this lab needs, which is the setting a US regulator would prefer.
- AI Runtime will be probed after the workspace exists. If the workspace API does not expose it, Project 3 training runs on CPU and the GPU policy/IaC remains the governance artifact.
- Classic GPU VMs stay behind `enable_gpu = false`.

## Quota evidence (2026-10-27, `az vm list-usage --location eastus`)

| Family | Current | Limit |
| --- | ---: | ---: |
| Total Regional vCPUs | 0 | 100 |
| Standard NC Family vCPUs | 0 | 48 |
| Standard NCASv3_T4 Family vCPUs | 0 | 0 |
| Standard NCADS_A100_v4 Family vCPUs | 0 | 0 |
| Standard NCadsH100v5 Family vCPUs | 0 | 0 |

NC family quota of 48 is not useful for current ML GPU SKUs. Do not request quota. See ADR-0004 and `docs/runbooks/enable-gpu-compute.md`.
