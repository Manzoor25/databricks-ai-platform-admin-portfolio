# FAQ

Thirty questions a platform admin actually gets. Short answers. If a question needs a runbook, the runbook wins.

1. Why can't I see this table? You were not granted. Check the grants matrix in ADR-0002. Asking an admin to SELECT * and paste it is not a workaround.
2. Why did my cluster die? Auto-termination. CPU policies are 20 minutes, GPU is 15. That is a control.
3. Why can't I pick a bigger VM? The policy allowlist. Bigger is a request with a cost reason, not a dropdown.
4. How do I get a GPU? Read `docs/runbooks/enable-gpu-compute.md`. Default answer is no.
5. Why is my token rejected after a week? Max token lifetime is 7 days. Verified in `evidence/workspace-conf.json`.
6. Can I export this notebook? No. `enableExportNotebook` is false.
7. Can I download query results? No. `enableResultsDownloading` is false.
8. Where do I put a secret? Key Vault, then a Databricks secret scope. Never in a notebook, never in git.
9. Why doesn't my external model config have a key? Because the key would be in git. The reference is `{{secrets/scope/key}}`.
10. What is Unity Gateway? The current name for AI Gateway. Rate limits, payload logging, guardrails, fallback.
11. What is AI Search? The current name for Mosaic AI Vector Search.
12. What happened to Delta Live Tables? Lakeflow Declarative Pipelines. Same job, current name.
13. Why is there no catalog? The workspace has no metastore. Account admin has to assign the existing East US one. ADR-0005. You cannot fix this from the workspace.
14. Can I create a metastore? No. The account is already at the East US limit, and you are not an account admin.
15. Why are storage and Key Vault public access off? Subscription policy. Terraform matches the policy. ADR-0003.
16. Is the workspace private? No. Cluster nodes have no public IP. The control plane is still public. Say that sentence out loud before you tell a regulator otherwise.
17. What data is in here? Public FDIC BankFind data and synthetic Faker rows. Nothing from a bank customer.
18. Why is the complaints table tagged confidential if it is fake? Because the control has to be practiced on something, and the label stops anyone treating it as real.
19. Who can see clear-text synthetic SSNs? `dbx-platform-admins`, via the column mask. Analysts see a mask. The agent sees a denial.
20. What is the difference between a mask and a row filter? A mask changes a column. A row filter removes rows. Both are in `sql/governance.sql`. Neither has been executed yet.
21. Why is the ingest job paused? It is defined and not deployed. Deploying it requires the metastore.
22. How do I see who queried a table? `system.access.audit`, query in `sql/system_tables.sql`. Needs system tables, which need the metastore.
23. How do I see spend? `system.billing.usage`, and the Azure budget at $75, $120, and $150.
24. A job is suddenly expensive. What do I check? SKU, tags, user, and whether a cluster ignored auto-termination. The policy exists so that last one should be rare.
25. Can CI apply Terraform? No. CI plans on pull requests only, and only if OIDC secrets exist. Apply is a person, from `scripts/up.ps1`.
26. Why OIDC and not a stored Azure key? A stored key is a secret in GitHub. A federated credential is not.
27. What is on-behalf-of-user? The agent acts as the caller, so it cannot exceed the caller's grants. Use it for interactive tools. Use a service principal for batch.
28. When do I use provisioned throughput instead of pay-per-token? When volume is forecast and finance wants a ceiling. Pay-per-token is the pilot default. ADR-0004.
29. What would make you turn on Private Link? Any non-public data, or an authorization boundary. Not this lab. ADR-0003.
30. What do I say if an interviewer asks whether the GPU job ran? No. The policy is real. The run was CPU. The log is `evidence/cpu-train.json`.
