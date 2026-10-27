# Runbook: Unity Catalog permission denied

1. Confirm a metastore is assigned. In this lab, on 2026-10-27, it was not. `databricks metastores current` returned "No metastore assigned." If that is still the error, stop. The fix is an account admin, not a grant. ADR-0005.
2. If a metastore is assigned, check USE CATALOG, then USE SCHEMA, then the privilege on the object. A SELECT grant without USE SCHEMA looks like a missing table.
3. For a mask that seems not to apply, check the function owner and whether the caller is in `dbx-platform-admins`. Admins see clear text by design.
4. For the agent, a denial on `synthetic_complaints` is the expected result. Do not "fix" it.
