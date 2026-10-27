# Two-minute pitch

I built a personal Databricks AI platform lab the way I would stand one up for a regulator, and I was honest about the wall I hit.

I deployed a Premium, VNet-injected workspace in East US with secure cluster connectivity, a Key Vault, ADLS Gen2, Log Analytics, and a $150 budget, all in Terraform. Two subscription policies blocked me: no storage account keys, and no public network access on storage or Key Vault. I changed the Terraform to match the policy instead of working around it.

I am a workspace admin on that workspace. I am not an account admin. Unity Catalog did not auto-attach, the account is already at its East US metastore limit, and the assign API returned 403. I wrote the grants, the column masks, the pipeline, and the gateway config anyway, and I labeled them not executed. I did not mint a PAT to get past the 403.

What I did verify: token lifetime cut from 730 days to 7, notebook export off, verbose audit logs on, 4,117 public FDIC failure records ingested, and a CPU training run with a promotion rule that requires a human approver. The GPU cluster policy is written and validated. No GPU job ran. That is the sentence I want an interviewer to hear, because it is the one a platform admin has to be willing to say.
