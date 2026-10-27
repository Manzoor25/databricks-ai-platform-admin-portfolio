# ADR-0002: Identity and least privilege

- Status: Accepted
- Date: 2026-10-27
- Docs checked: 2026-10-27
- Doc: https://learn.microsoft.com/en-us/azure/databricks/admin/users-groups/automatic-identity-management

## Context

A regulator does not manage Databricks users by pasting emails into the workspace admin page. Identity has to come from Entra ID, and every grant has to be explainable.

## Decision

1. Use **automatic identity management** (the current replacement for most hand-rolled SCIM provisioning on Azure Databricks) so Entra ID users and groups appear in the account when they are assigned access. Document the older SCIM connector only as the fallback if automatic identity management is not enabled on the account.
2. Create these Entra ID security groups, then grant inside Databricks against the synced groups, not against individuals:
   - `dbx-platform-admins`
   - `dbx-data-engineers`
   - `dbx-data-scientists`
   - `dbx-analysts`
   - `dbx-ai-agents`
3. Create two service principals:
   - `sp-dbx-cicd` for GitHub Actions (federated credential, no stored secret).
   - `sp-dbx-regulatory-agent` for the Project 2 agent. Grants are USE CATALOG, USE SCHEMA, SELECT on named tables, EXECUTE on the UC function, and USE on the vector index. No grant on the PII table.
4. Workspace admin is a break-glass role. Day-to-day admin uses the `platform-admins` group.

## Consequences

- If the account admin console is not reachable with the current user (no account admin role), group sync is documented and the workspace-level groups are created as a fallback. That fallback is labeled as such in the README. It is not claimed to be account-level SCIM.
- The agent service principal is the identity interviewers should hear about: "the agent is not me, and it cannot read PII."

## Grants matrix

| Principal | dev | prod tables | prod PII | vector index | serving endpoint | SQL warehouse |
| --- | --- | --- | --- | --- | --- | --- |
| platform-admins | ALL | ALL | clear text | MANAGE | CAN_MANAGE | CAN_MANAGE |
| data-engineers | WRITE | WRITE on bronze/silver | masked | WRITE | CAN_VIEW | CAN_USE |
| data-scientists | USE + CREATE MODEL | SELECT gold | masked | SELECT | CAN_QUERY | CAN_USE |
| analysts | none | SELECT gold non-PII | denied | none | none | CAN_USE (Genie) |
| ai-agents SP | none | SELECT named gold tables | denied | SELECT | CAN_QUERY | none |
| cicd SP | deploy | deploy bundles | none | deploy | CAN_MANAGE in dev | none |
