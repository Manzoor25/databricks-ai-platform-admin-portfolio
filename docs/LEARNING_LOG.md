# Learning log

Written so you can explain each step in an interview. Every entry is something this build actually did, or an explicit "not yet verified" note. Do not claim a step was verified until the evidence section says so.

## 2026-10-27 — Region, quota, and product names

**What I did.** Checked Azure CLI auth (subscription `MCAPS-Hybrid-REQ-120861-2025-mamoh`, user `mamoh@microsoft.com`). Listed East US VM quota. Read the current Azure Databricks region, model, and Designated Services pages. Installed Terraform 1.16.6 and Databricks CLI 1.22.1. Recorded the decision in ADR-0001.

**Why.** A platform admin does not pick a region from memory. Model serving, pay-per-token APIs, vector search, and serverless are not in every region, and the names change.

**Admin concept.** Feature availability is a control, not a convenience. For a US regulator, keep processing inside the United States geo and leave cross-geo processing off unless a named feature requires it and a named approver accepts it.

**What changed since older training material.**

- AI Gateway is documented as **Unity Gateway**.
- Mosaic AI Vector Search is documented as **AI Search** (Lakehouse Real-Time is the broader real-time surface).
- Delta Live Tables is **Lakeflow Declarative Pipelines**.
- Serverless GPU is **AI Runtime** (A10 / H100, Databricks-managed, not your VM quota). It is Available in the United States geo as of the 2026-10-26 Designated Services page.
- Asset bundles are still `databricks bundle` in CLI 1.22.1; docs also say Declarative Automation Bundles.

**Common mistake.** Requesting GPU quota before checking whether the workload needs a classic GPU VM at all. Foundation Model APIs and AI Runtime do not use your NC-family quota. This subscription's T4/A100/H100 families are at limit 0. NC-family limit is 48, which does not unlock current ML GPU SKUs. Decision: do not request quota.

**Interview question.** "Your data scientists say they need GPUs. What do you ask before you open a quota request?"

**Strong answer.** "I ask what the workload is. If it is prompting a foundation model, I point them at pay-per-token or provisioned throughput and keep their data in-geo. If it is fine-tuning or custom deep learning, I check AI Runtime first, because that is Databricks-managed GPU and does not consume subscription VM quota. I only request classic GPU quota when they need a cluster they control, and I put that request through a policy: ML GPU runtime, allowlisted node types, single node, 15-minute auto-termination, a DBU/hour cap, and mandatory tags. I do not start the VM until quota and budget are approved."

## 2026-10-27 — Foundation Terraform

**What I did.** Wrote Terraform for a resource group, VNet with delegated public/private subnets, ADLS Gen2 (HNS on), Key Vault (RBAC), Log Analytics, a $150 subscription budget filtered to the resource group with 50/80/100 alerts, and a Premium VNet-injected workspace with `no_public_ip` (secure cluster connectivity). Diagnostic settings send workspace logs to Log Analytics.

**Why.** A federal-style platform is reproducible. Click-ops cannot be reviewed, diffed, or rebuilt after an incident.

**Admin concept.** Secure cluster connectivity (`no_public_ip = true`) removes public IPs from cluster nodes. It is not the same as front-end Private Link. Private Link is behind `enable_private_link = false` because of cost; ADR-0003 explains when a regulator would require it.

**Common mistake.** Treating "no public IP" as "the workspace is private." The workspace control plane is still reachable on the public front end unless Private Link and public network access disabled are both set.

**Interview question.** "What is the difference between secure cluster connectivity and front-end Private Link?"

**Strong answer.** "Secure cluster connectivity means cluster nodes have no public IP; they reach the control plane over the Databricks-managed path. Front-end Private Link means users and CI reach the workspace itself over a private endpoint, and you can disable public network access. A regulator with a 'no public management plane' requirement needs both. A lab that is teaching the data-plane control can ship SCC now and keep Private Link as a flagged module."

## 2026-10-27 — Apply, policy fight, and the account-admin wall

**What I did.** `terraform apply` created the resource group, VNet, Premium workspace, Log Analytics, $150 budget, Key Vault, and ADLS Gen2. Two subscription policies pushed back:

1. Storage key auth is denied. Fix: `shared_access_key_enabled = false` and `storage_use_azuread = true`.
2. Public network access on storage and Key Vault is forced off. Fix: set `public_network_access_enabled = false` in Terraform so the next plan does not fight the policy.
3. Databricks metric export is not enabled. Diagnostic setting sends logs only. The setting already existed from a partial apply, so it was imported into state.

Workspace admin API calls succeeded. Token lifetime is now 7 days (was 730). Notebook export is off. Verbose audit logs are on. Evidence: `evidence/workspace-conf.json`.

Unity Catalog did not auto-attach. Creating a metastore failed because account `fe15873c-2234-4e08-ad9e-953086cae5cf` is already at the East US metastore limit. Assigning the existing one returned 403: the user is a workspace admin, not an account admin. Recorded in ADR-0005. Not papered over.

**Why this is the lesson.** Platform admin work is mostly "the API said no, here is the control that still shipped." A candidate who only describes the happy path has not operated a platform.

**Admin concept.** Workspace admin and account admin are different roles. Metastore create/assign, account groups, and automatic identity management are account-admin. Cluster policies, workspace conf, and token lifetime are workspace-admin. Know which console you are in before you promise a control.

**Common mistake.** Creating a long-lived PAT "just to get past" an account-admin 403. That is the opposite of the control you are trying to demonstrate. The lab keeps token lifetime at 7 days and does not mint a PAT.

**Interview question.** "Your new workspace has no metastore and you are not an account admin. What do you ship today?"

**Strong answer.** "I confirm the 403 and write down the account id and the exact error. I do not create a second metastore; the account is already at the regional limit. I send the account admin a one-step assignment request for the existing East US metastore. Meanwhile I ship the controls I do own: workspace conf, cluster policies, diagnostic settings, the budget, and the pipeline code that will run the moment the metastore is assigned. I do not mark Unity Catalog as done."

## Not yet verified

- `terraform apply` of the foundation (in progress when this entry was first written; update with resource IDs when it finishes).
- Unity Catalog metastore assignment (needs the Databricks account ID from the account console).
- AI Runtime enablement on the new workspace.
- Any GPU workload. None has been executed. Do not say otherwise.
