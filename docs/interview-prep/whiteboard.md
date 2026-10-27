# Whiteboard scenarios

## 1. Design AI governance for 500 users across 3 divisions

One Databricks account. One metastore per region, not per division. Entra groups per division and per persona (engineer, scientist, analyst, agent). Catalogs by environment (`dev`, `prod`), schemas by domain, not by division. Division access is a grant, not a copy of the data. Genie spaces are per domain and never include a table tagged `pii`. Agents are service principals with table-level SELECT. Unity Gateway on every endpoint: per-user rate limit, inference table, PII block. A platform team owns policies, budget, and the metastore. Data owners own grants. Model risk owns external-model approval.

## 2. A cluster will not start

Read the event log before you change anything. Check, in order: policy denial (node type, runtime, missing tag), quota (`az vm list-usage`), subnet free IPs, and whether the workspace is VNet-injected and the NSG association drifted. Do not raise quota because a policy denied a GPU node. If the user asked for a GPU node and the policy is the CPU policy, the answer is the request process, not a bigger allowlist.

## 3. Spend doubled overnight

`system.billing.usage` by SKU, tag, and user for the last 48 hours. Look for a classic cluster that outlived auto-termination, a serverless warehouse someone set to a large size, or a model endpoint that did not scale to zero. The budget alert should already have fired at 80 percent. If it did not, the alert is the bug you fix after you stop the resource.

## 4. An analyst pasted an SSN into Genie

Two failures, not one. The space should not have been able to send that to a model: the gateway PII guardrail blocks it. And the analyst should not have had an SSN to paste: the column mask exists so the clear value is not on their screen. Check the inference table for the blocked request. Then check the grant. Then talk to the person. Do not only talk to the person.

## 5. Design for GPU when you have no quota

Say the decision tree. Foundation Model API if they are calling a model. AI Runtime if they are fine-tuning and the geo lists it. Classic quota last, one node, 15-minute auto-termination, ML runtime, allowlisted SKUs, tags, DBU cap. Write the policy before the quota arrives, so the day quota lands the unsafe shape is not an option. Do not tell the interviewer you trained on a GPU.
