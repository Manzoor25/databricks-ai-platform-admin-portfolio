# ADR-0005: Unity Catalog is blocked on account-admin, and that is recorded honestly

- Status: Accepted (blocker, with a working alternative for everything that does not need a metastore)
- Date: 2026-10-27

## What was verified

- Workspace `dbw-dbx-ai-admin-lab` is Premium, East US, VNet-injected, `enableNoPublicIp = true`. URL: `https://adb-7405619764740124.4.azuredatabricks.net`. Workspace id `7405619764740124`.
- `databricks metastores current` returned: `No metastore assigned for the current workspace.`
- Creating a metastore returned: `This account with id fe15873c-2234-4e08-ad9e-953086cae5cf has reached the limit for metastores in region eastus.`
- Listing and assigning that existing metastore returned HTTP 403: `This API is disabled for users without account admin status.`
- The signed-in user is a **workspace admin** (`admins` group) and is **not** an account admin.

## Decision

Do not pretend Unity Catalog is attached. Do not create a PAT to work around the 403. Do not ask the user to click through the account console unless they are actually an account admin; the 403 says they are not.

Everything that does not need a metastore is built and, where possible, executed:

- Workspace configuration (verified, see `evidence/workspace-conf.json`).
- Cluster policy JSON, validated by `terraform validate` and a plan with `enable_gpu` on and off.
- Pipelines, masks, grants, vector search, and serving are written as code and called out as **not executed** until a metastore is assigned.

## What an account admin does to unblock (one action)

1. Open the [Azure Databricks account console](https://accounts.azuredatabricks.net) as an account admin.
2. Confirm the existing East US metastore (the account is already at the regional limit, so do not create another).
3. Assign workspace `7405619764740124` to that metastore.
4. Re-run `scripts/verify.ps1`. The script detects the assignment and continues; it does not need a code change.

## Interview line

"I got a 403, not a green check. The workspace was admin-ready. The account was not mine to administer. I wrote the metastore assignment, the grants, and the masks anyway, and I labeled them not executed. Claiming Unity Catalog was on would have been the failure."
