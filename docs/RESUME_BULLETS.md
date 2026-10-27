# Resume bullets

Only what this repo actually did. Do not paste a bullet into a resume if you cannot point at the file.

- Built a Premium, VNet-injected Azure Databricks workspace in East US with secure cluster connectivity (`no_public_ip`), tagged resources, and a $150/month budget with 50/80/100 alerts, all in Terraform.
- Set workspace admin controls and verified them: token lifetime 7 days (down from 730), notebook export off, results download off, verbose audit logs on.
- Diagnosed two subscription policy denials (storage shared-key auth, public network access on storage and Key Vault) and encoded the compliant settings in Terraform instead of fighting the policy.
- Wrote Unity Catalog grants, column masks, and row filters for synthetic PII, and stopped when account-level metastore assignment returned 403. Documented the blocker instead of claiming the catalogs existed.
- Ingested 4,117 public FDIC failed-bank records from `api.fdic.gov` and generated 50 clearly labeled synthetic complaint rows for a masking demo. No non-public data.
- Defined persona cluster policies, including a GPU policy (ML runtime, GPU node allowlist, single node, 15-minute auto-termination, DBU cap) behind `enable_gpu = false`. Validated with `terraform validate`. Did not start a GPU VM.
- Ran the bank-distress training entry point on CPU (`device=cpu`) and recorded the output. The same job takes `cuda` when a GPU exists. No GPU run is claimed.
- Wrote the AI Gateway (Unity Gateway) rate-limit, guardrail, and external-model templates with secret references only (`{{secrets/...}}`). No key in git, and the disabled Anthropic and OpenAI templates stay disabled.
