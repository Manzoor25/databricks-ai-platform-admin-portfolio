# 12-month Databricks Data + AI roadmap for a federal financial regulator

This is a document you could hand a program manager. It is not a claim that this lab is that regulator. Current-state assumptions are labeled. FedRAMP statements cite public pages only.

## Current state (this lab, 2026-10-27)

- One Premium workspace, East US, VNet injection, secure cluster connectivity, public control plane.
- No Unity Catalog metastore assigned, because the caller is not an account admin and the account is at the East US metastore limit.
- No non-public data. Public FDIC API plus synthetic PII.
- No GPU VM. GPU policy written, training executed on CPU.
- $150/month budget. Fine for a lab. Not a program budget.

## Maturity model

| Level | Name | You are here when |
| --- | --- | --- |
| 0 | Workspace sprawl | Users create workspaces, no metastore, no tags |
| 1 | Foundation | One account, metastores per region, Entra groups, budgets, diagnostic settings |
| 2 | Governed self-service | Unity Catalog grants, policies, Genie on gold only, no PII in Genie |
| 3 | GenAI pilot | One agent, one gateway, eval set, model card, human approval |
| 4 | Scaled AI with model risk | Aliases, monitoring, periodic validation, written owners |

This lab is late level 1 on Azure controls and early level 1 on Databricks, blocked at the account boundary.

## Phased rollout

**Months 1-3, Foundation.** Assign the existing metastore. Turn on automatic identity management. Land Entra groups. Enforce cluster policies. Turn on system tables. Agree the tag set: `pii`, `sensitivity`, `owner`, `cost-center`. No model is deployed in this phase.

**Months 4-6, Governed self-service.** Gold tables for the public bank dataset. Genie space with certified questions. Column masks on anything tagged `pii`. Analysts never get a cluster. Serverless SQL only, auto-stop.

**Months 7-9, GenAI pilot.** One use case: a regulatory-document assistant over public guidance. Pay-per-token, in-geo, Unity Gateway in front, inference table on, PII block. Eval set of at least 25 questions. Model card. No external model outside the tenant.

**Months 10-12, Scaled AI and model risk.** Promotion job from `@challenger` to `@champion` with a human `approved_by`. Drift monitoring on the inference table. A quarterly access review. A written decision on provisioned throughput if the pilot volume justifies it.

## GPU capacity

Do not buy GPU quota in month 1. Sequence:

1. Foundation Model APIs for anything that is "call a model."
2. AI Runtime (serverless GPU, Databricks-managed, in the United States geo) for fine-tuning experiments.
3. Classic GPU quota only for a workload that must control the VM, with a one-node cap and 15-minute auto-termination.

A federal quota request is a procurement action: workload justification, data-classification check, cost from the current Azure price page, security review of the image, then the quota ticket. This lab did not file one.

## FedRAMP

Say only this. Databricks publishes its own FedRAMP status; verify it on the vendor's page and on the FedRAMP marketplace before you repeat it, because the scope (which SKU, which region, which features) is narrower than the marketing sentence. Azure Databricks in Azure commercial is not the same boundary as Azure Government. This lab is in Azure commercial East US, `enableFedRampCertification` on the workspace is false (read from the ARM properties on 2026-10-27), and it is not authorized for any federal system. Citation to re-check before an interview: the FedRAMP marketplace and the Databricks trust center, not this paragraph.

## FinOps

- Tag everything. This lab tags `project`, `owner`, `cost-center`, `environment`.
- Budget alerts at 50/80/100. A platform admin who learns about spend from the invoice is late.
- Serverless SQL and model serving scale to zero or auto-stop. Classic clusters auto-terminate.
- A monthly review of `system.billing.usage` by SKU, tag, and user. The query is in `sql/system_tables.sql`.
- GPU is a separate line. If it is not zero, someone owns the explanation.

## Operating model

A small center of excellence, not a ticket wall.

| Activity | Platform admin | Data owner | Model risk | User |
| --- | --- | --- | --- | --- |
| Metastore, policies, budget | A | C | I | I |
| Grants on a table | C | A | I | R |
| Genie space content | C | A | C | R |
| New external model | C | C | A | I |
| GPU quota request | R | C | C | A (the requester) |

A = accountable, R = responsible, C = consulted, I = informed.

## KPIs

- Percent of tables with an owner and a classification tag.
- Percent of clusters created under a policy (target: 100).
- Token lifetime over 7 days (target: 0).
- PII-tagged tables with a mask (target: 100).
- Agent endpoints without an inference table (target: 0).
- Monthly spend versus budget.
- Time to revoke a leaver. Entra disable should be the only step.

## Risks

- Account admin is a single team. This lab hit that risk on day one.
- Cross-geo processing turned on "to try a model" and forgotten.
- A Genie space pointed at a PII table because the table was convenient.
- A GPU cluster with no auto-termination. The policy exists to make that hard.
- A resume bullet that claims a control ran when only the code exists. Do not do that. The coverage matrix is the source of truth.
