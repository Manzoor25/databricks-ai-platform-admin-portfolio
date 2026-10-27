# Databricks Data + AI Platform Administrator accreditation

Source, fetched 2026-10-27: https://www.databricks.com/learn/certification/platform-administrator-accreditation

The page says: 25 multiple-choice questions, unlimited time, not proctored, free for customers and partners, valid for one year. No programming questions. A minimally qualified candidate can describe user administration, compute, and governance. Topics named on the page:

- Users and groups, identity providers, admin roles, workspace APIs
- Clusters (init scripts, policies, types, pools), SQL warehouses, MLflow model serving, jobs and pipelines
- Permissions, data governance, secret management, Delta Sharing, model governance

Map those to this repo. If a row says "not executed," you can still explain it, and you should say you have not clicked it.

| Topic | Where you practiced | Honest status |
| --- | --- | --- |
| Workspace admin vs account admin | ADR-0005, the 403 | You hit this. Best story in the repo. |
| Identity providers and groups | ADR-0002 | Designed. Groups not created in Entra in this session. |
| Token lifetime and workspace APIs | `evidence/workspace-conf.json` | Verified. 730 days down to 7. |
| Cluster policies and pools | `infra/compute.tf` | Written and validated. Not attached to a live cluster. |
| SQL warehouses | Bundle and docs | Designed, serverless, auto-stop. Not created. |
| Jobs and pipelines | `databricks.yml`, notebook | Written. Job is paused and not deployed. |
| Secrets | Key Vault module, external model templates | Vault exists. No secret stored. |
| Unity Catalog, grants, masks | `sql/governance.sql` | Written. Not executed. |
| Model governance | `src/train.py` promotion rule, model card notes | CPU run verified. UC registration not done. |
| Delta Sharing | not built | Say so. Read the docs page before the exam. |

## Practice questions

Answer out loud. The strong answer names the control and the limit.

1. What is the difference between a workspace admin and an account admin?
2. Why is one metastore per region the rule?
3. A user cannot see a table. List the three checks, in order.
4. What does a cluster policy enforce that a spoken agreement does not?
5. Why force auto-termination in the policy instead of asking users to set it?
6. What is an instance pool for, and why is `min_idle = 0` the lab default?
7. When do you pick serverless SQL over a classic warehouse?
8. What does secure cluster connectivity change, and what does it not change?
9. Why would a regulator still require front-end Private Link?
10. Where does a secret live, and what must never appear in a notebook?
11. What is a column mask, and who bypasses it in this design?
12. What is a row filter for?
13. Why tag a synthetic table `pii=true`?
14. What is Unity Gateway, and which older name should you still recognize?
15. What do you log on a model endpoint, and why?
16. What is an inference table?
17. Pay-per-token versus provisioned throughput: which is the pilot default, and why?
18. When does a workload actually need a GPU?
19. What is AI Runtime, and whose quota does it use?
20. Why is a 15-minute GPU auto-termination non-negotiable?
21. What does `enableExportNotebook=false` protect?
22. Why is a 7-day token lifetime a control and not an inconvenience?
23. How do you find who granted a permission last week?
24. How do you find which job spent the DBU?
25. What is the first query you run when finance asks about a spike?
26. Why are tags on the cluster policy mandatory rather than optional?
27. What is the difference between CAN_QUERY and CAN_MANAGE on an endpoint?
28. Why does the agent run as a service principal?
29. When would you use on-behalf-of-user instead?
30. What is a model alias, and who is allowed to move `@champion`?
31. What has to be true before `@challenger` is promoted in this repo?
32. What is Delta Sharing for? (Read the docs; this repo does not implement it.)
33. Why does CI plan and never apply?
34. What is OIDC for in the GitHub workflow, and what does it replace?
35. A subscription policy denies storage account keys. What do you change, and what do you not do?
36. Why is "the workspace is private" a dangerous sentence if only SCC is on?
37. What system table holds audit events?
38. What system table holds usage?
39. Name two things you would turn off before non-public data arrives.
40. What will you say when asked if this lab's GPU job ran?

Strong answer to 40: "No. I validated the policy and I ran the same code on CPU. I will not say I trained on a GPU."
