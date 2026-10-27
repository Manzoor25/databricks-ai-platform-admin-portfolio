# Day 1 on Databricks, for an analyst

You will not create a cluster. You will not see the synthetic PII table in clear text. That is the design.

1. Sign in with your Entra ID account. There is no separate Databricks password.
2. Open SQL, then the warehouse named for this lab. If it is stopped, starting it is allowed. Leaving it running is not; it auto-stops.
3. Open the Genie space "FDIC Bank Health Explorer" when it has been published. Ask the sample questions. If Genie says it cannot see a table, that is a grant, not a bug. File a request; do not ask someone to paste the rows into chat.
4. The complaints table is synthetic and masked. If you see a real-looking SSN, stop and tell a platform admin. You should see `***-**-1234` or no rows.
5. Dashboards are for reading. Export is disabled on this workspace. A screenshot of aggregate numbers is fine. A download of row-level data is not, and the API will refuse it.

If a number looks wrong, the first question is "which table, which filter," not "can you make the chart say X."
