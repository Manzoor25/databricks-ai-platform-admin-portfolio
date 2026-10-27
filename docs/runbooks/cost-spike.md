# Runbook: cost spike

1. Open the Azure budget alerts first. Note which threshold fired and when.
2. Run the usage query in `project-1-governed-lakehouse-platform/sql/system_tables.sql` for the last 48 hours, grouped by SKU and tags.
3. Stop the offender. A warehouse, a cluster, or an endpoint that is not scale-to-zero. Stopping is reversible. Investigating while it bills is not.
4. Check for a cluster that escaped auto-termination. If you find one, the policy failed or someone had unrestricted create. Fix that after the spend stops.
5. GPU spend should be zero in this lab. If it is not, someone started a node outside the flag. Terminate it and read ADR-0004 before you do anything else.
