# STAR stories

First person. Only events that happened in this build. Dates are 2026-10-27.

## 1. The account-admin wall

Situation: the new Premium workspace had no metastore. The brief needed Unity Catalog.
Task: attach a metastore and keep going.
Action: I tried to create one. The API said the account was already at the East US limit. I tried to list and assign the existing one. Both returned 403, not an account admin. I wrote ADR-0005 with the account id and the exact error, and I did not create a PAT.
Result: the lab is honest. An account admin has a one-step unblock. I can explain workspace admin versus account admin from a scar, not a slide.

## 2. Subscription policy on storage keys

Situation: Terraform failed creating the storage containers with `KeyBasedAuthenticationNotPermitted`.
Task: get a working ADLS Gen2 account without weakening the policy.
Action: I set `shared_access_key_enabled = false` and `storage_use_azuread = true`, and re-applied.
Result: the account and the three containers exist, and the next plan does not try to turn keys back on.

## 3. Public network access forced off

Situation: a second policy set public network access to false on Key Vault and storage. My Terraform wanted it true, so every plan would have fought the policy.
Task: make the code match the control that is already in force.
Action: I set `public_network_access_enabled = false` and recorded in ADR-0003 that this is policy, not Private Link. The workspace control plane is still public.
Result: the plan is stable. I can also say, correctly, that the workspace is not private.

## 4. Token lifetime

Situation: a new workspace allows tokens for 730 days.
Task: put a regulator-shaped limit on without locking myself out.
Action: I PATCHed workspace conf to 7 days, turned notebook export and results download off, and turned verbose audit logs on. I saved the before and after JSON.
Result: `evidence/workspace-conf.json` is the proof. I did not create a token to test the limit, because creating one was the thing I was trying to avoid.

## 5. GPU under a quota constraint

Situation: T4, A100, and H100 family limits are 0. The role still expects GPU governance.
Task: show the control without pretending a GPU job ran.
Action: I wrote the GPU policy (ML runtime, node allowlist, single node, 15-minute auto-termination, DBU cap) behind `enable_gpu = false`. I checked AI Runtime, which is Databricks-managed and does not use my quota, and I did not get a session attached. I ran the training entry point with `device=cpu` and saved the output.
Result: I can talk about GPU administration. I cannot claim a GPU run. I don't.

## 6. Diagnostic setting import

Situation: a partial apply created the diagnostic setting, then a later apply tried to create it again.
Task: own the resource in Terraform without deleting it.
Action: I imported it by id, and I dropped the metric category because the API returned "Metric export is not enabled."
Result: logs flow to Log Analytics. Metrics do not, and the README says so.

## 7. Public data only

Situation: the domain is a bank regulator. Using real customer data would have been the easy way to make demos look serious.
Task: make the governance demo real without real PII.
Action: I pulled the public FDIC failures API (4,117 rows) and generated complaints with Faker, labeled `synthetic-faker` on every row.
Result: the masking demo has something to mask, and nothing in the repo is a person.

## 8. CI that cannot apply

Situation: a portfolio repo with cloud credentials in GitHub Actions is how labs leak.
Task: lint and plan on pull requests, never apply.
Action: the workflow uses OIDC placeholders and skips the plan if the secrets are absent. Apply stays a local command.
Result: a reviewer can see the guard. The workflow has not been run yet, because the repo was not on GitHub when this file was written. I will not claim a green check I have not seen.
