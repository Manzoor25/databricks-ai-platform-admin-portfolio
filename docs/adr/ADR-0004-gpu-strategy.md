# ADR-0004: GPU strategy under a quota constraint

- Status: Accepted
- Date: 2026-10-27
- Docs checked: 2026-10-27
- Docs:
  - https://learn.microsoft.com/en-us/azure/databricks/machine-learning/ai-runtime/overview (2026-10-21)
  - https://learn.microsoft.com/en-us/azure/databricks/resources/designated-services (2026-10-26)
  - https://learn.microsoft.com/en-us/azure/databricks/machine-learning/foundation-model-apis/

## Context

The subscription cannot start current ML GPU VMs (T4, A100, H100 family limits are 0). The brief forbids waiting on a quota request. A Databricks AI platform admin still has to show they can govern GPU compute.

## When a regulator actually needs GPUs

| Workload | GPU needed? | Use this instead |
| --- | --- | --- |
| Prompt a foundation model, RAG, agents, Genie, AI Functions | No | Foundation Model APIs (pay-per-token) or an external model endpoint |
| Steady high-volume inference on one model | No, unless you must self-host | Provisioned throughput, then review cost vs. pay-per-token |
| Fine-tune an open model, train a deep network, large embedding job you will not send to a vendor | Yes | AI Runtime (serverless GPU) first; classic GPU cluster only if you must control the VM image |
| Serve your own custom model | Usually CPU is enough | CPU model serving with scale-to-zero; GPU serving only if latency or model size requires it |

Pay-per-token avoids GPU procurement, capacity planning, and idle GPU cost. The tradeoff is data-processing residency (stay in-geo; do not enable cross-geo without an approval) and less cost predictability than provisioned throughput. For a regulator, pay-per-token is the right default for a pilot. Provisioned throughput is the right default once a use case has a forecast and a model-risk approval.

## Decision

1. **Do not request classic GPU quota** for this lab.
2. **Probe AI Runtime** after the workspace exists. It is Databricks-managed serverless GPU and is listed Available in the United States geo. It does not use this subscription's VM quota. If the workspace can run a 1xA10 job, Project 3 uses it and says so. If it cannot, Project 3 runs on CPU and the README says so. Either way, no classic GPU VM is started.
3. **Define the classic GPU cluster policy and pool in Terraform/JSON now**, behind `enable_gpu = false`. The policy forces ML runtime, an allowlist of GPU node types, single node, 15-minute auto-termination, a DBU/hour cap, and mandatory tags. Defining a policy does not start a VM.
4. Training code takes `device` as a job parameter (`cpu` default, `cuda` ready) so the same job runs on a GPU later without a rewrite.
5. A federal procurement path for classic GPU quota is: workload justification, data-classification check, cost-per-hour from the current Azure price page, security review of the image and init scripts, then a quota request. That path is a runbook, not a click this lab performs.

## Cost controls that ship regardless of quota

- Auto-termination 15 minutes on the GPU policy, 20 minutes on every other policy.
- DBU/hour cap on every policy.
- Mandatory tags: project, owner, cost-center, environment.
- No pool is pre-warmed. A pool with `min_idle = 0` still costs nothing until a cluster starts.
- Budget alert at $75 / $120 / $150.

## Consequences

- Honesty rule: no document in this repo claims a GPU workload ran unless `evidence/` contains the run output.
- Interview line: "I governed GPU compute before I had GPU quota. The policy is the control. The VM is the exception."
