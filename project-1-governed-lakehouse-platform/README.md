# Project 1 — Governed lakehouse

## Verified

- Premium workspace `dbw-dbx-ai-admin-lab` in East US, VNet-injected, `enableNoPublicIp = true`.
- Workspace conf after PATCH: token lifetime 7 days, notebook export false, results download false, verbose audit true. See `../evidence/workspace-conf.json`.
- Public FDIC ingest from this laptop: 4,117 failure records, 50 institutions, 50 synthetic complaints. Sample of 5 rows in `../evidence/fdic-sample/`.
- Unit tests in `tests/` passed (4) on 2026-10-27.

## Written, not executed

- `sql/governance.sql` — catalogs, masks, row filter. Needs a metastore. ADR-0005.
- `sql/system_tables.sql` and `sql/log_analytics_kql.kql` — the queries an admin runs. Not run against live data; system tables are not available without the metastore, and Log Analytics has little to show yet.
- `databricks.yml` — paused ingest job. Not deployed. `databricks bundle validate` was not run in this session; do not claim it was.

## Grants matrix

See `../docs/adr/ADR-0002-identity-and-least-privilege.md`.
