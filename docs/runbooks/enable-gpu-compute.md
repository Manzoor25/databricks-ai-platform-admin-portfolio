# Runbook: enable GPU compute

Status of this lab on 2026-10-27: **no GPU workload has been executed.** Classic GPU family limits for T4, A100, and H100 are 0. Do not start here by requesting quota.

## 1. Decide whether a GPU is the right tool

Read ADR-0004. If the user wants to call a foundation model, stop. Use Foundation Model APIs. A GPU is for fine-tuning, custom deep learning, or a model you must self-host.

## 2. Try AI Runtime before classic quota

AI Runtime is Databricks-managed serverless GPU. It does not use this subscription's VM quota. United States geo lists it as Available (Designated Services page, checked 2026-10-26).

1. In the workspace, open a notebook, Compute, Serverless GPU, accelerator `1xA10`.
2. Or from the CLI: `databricks air run --file workload.yaml --watch` ([AI Runtime overview](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/ai-runtime/overview)).
3. If the control is missing, the workspace is not enabled for AI Runtime. That is an account or preview flag, not a quota request. Record the error and fall back to CPU. Do not claim the GPU run happened.

This lab could not attach a notebook to Serverless GPU from the CLI in this session. Training defaults to `device=cpu`.

## 3. Check classic quota (only if AI Runtime will not do)

```powershell
az vm list-usage --location eastus --query "[?contains(localName, 'NC')].{name:localName, current:currentValue, limit:limit}" -o table
```

Request, in the Azure portal, Quota, the family that matches the policy allowlist:

- `Standard_NC4as_T4_v3` or `Standard_NC8as_T4_v3` for small training (NCASv3_T4 family).
- `Standard_NC24ads_A100_v4` only for a model that does not fit an A10 (NCADS_A100_v4 family).

Ask for the smallest number of vCPUs that starts one node. A federal request needs a workload justification, a data-classification check, and a cost number from the current Azure pricing page before it is submitted. This lab did not submit one.

## 4. Cost

Cite the live page, do not hard-code a price that will rot: [Azure Databricks pricing](https://azure.microsoft.com/pricing/details/databricks/) and [Azure VM pricing](https://azure.microsoft.com/pricing/details/virtual-machines/linux/). A single GPU node left running is the cost incident. The policy forces 15-minute auto-termination so a forgotten cluster cannot bill overnight.

## 5. Flip the flag

1. Set `enable_gpu = true` in `infra/terraform.tfvars`.
2. `terraform plan` and confirm the plan creates the pool definition and does not start a VM (`min_idle_instances = 0`).
3. Pass `--device cuda` to the Project 3 job only after a GPU cluster or AI Runtime session is actually attached.
4. Put the job log in `evidence/`. Until that file exists, the answer to "did you train on GPU?" is no.

## 6. Turn it back off

Set `enable_gpu = false` and apply. Terminate any all-purpose cluster in the UI. Confirm with the billing system table that GPU DBU dropped to zero the same day.
