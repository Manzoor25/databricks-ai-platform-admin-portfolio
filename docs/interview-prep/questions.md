# Technical questions

Fifty. Answers are short on purpose. Expand them out loud from the repo, not from memory of a blog post.

## Unity Catalog

1. What is a metastore? The top-level container for catalogs, grants, and storage credentials in a region. One per region.
2. Why did this workspace not have one? It was not auto-assigned, and I am not an account admin. ADR-0005.
3. Catalog versus schema versus table? Environment, domain, dataset. Grants get narrower as you go down.
4. What is a storage credential? The identity Unity Catalog uses to reach cloud storage. On Azure, an access connector managed identity.
5. External location versus volume? An external location is a governed path. A volume is a governed place for files, including unstructured documents.
6. Managed versus external table? Managed: UC owns the files. External: you own the path, UC owns the metadata.
7. What does a column mask not do? It does not encrypt the file. It changes what a query returns for that principal.
8. Who bypasses the mask here? Members of `dbx-platform-admins`, because the function checks `is_account_group_member`.
9. What is a row filter for? Removing rows, not hiding columns. Example: a state team sees one state.
10. Why bind `prod` read-only to the dev workspace? So a dev workspace cannot become a back door to production writes.

## Compute

11. What is secure cluster connectivity? Cluster nodes have no public IP. It is not front-end Private Link.
12. Why 20 minutes, not 60? A forgotten cluster is the cost incident. Twenty minutes is enough to notice, not enough to bill overnight.
13. Why is the GPU policy 15? GPU nodes cost more per minute. The shorter cap is the point.
14. What does a policy allowlist buy you? Users cannot pick an unapproved SKU, even if they know the API.
15. What is a pool? Pre-warmed instances to cut start time. `min_idle = 0` means it does not cost money while empty.
16. Serverless SQL versus classic warehouse? Serverless for Genie and ad hoc, auto-stop, no VM management. Classic only if you need a feature serverless does not have.
17. What is a DBU? Databricks' billing unit. Policies cap DBU/hour so a bad cluster shape fails at creation, not at the invoice.
18. Why mandatory tags? So the billing table can be grouped. A tag you hope users set is a tag you will not have.

## GPU

19. Which GPU families are at zero in this subscription? T4 (NCASv3), A100, H100. Checked 2026-10-27.
20. Does AI Runtime use that quota? No. It is Databricks-managed serverless GPU. United States geo lists it Available.
21. Why not request quota immediately? Because most of the asked-for workloads do not need a VM. Quota is a procurement action.
22. What is on the GPU policy? ML runtime, GPU node allowlist, single node, 15-minute auto-termination, DBU cap, tags.
23. How do you share a GPU cluster? You don't, by default. Single-user, short-lived. Sharing a GPU cluster is how one person's job bills another person's budget.
24. What would you request, if you had to? The smallest T4 node that runs the job, not an A100, until someone shows memory pressure.
25. What is the device flag for? So the same code runs on CPU now and CUDA later without a rewrite. It is not evidence that CUDA ran.

## AI Gateway / Unity Gateway

26. What is the current product name? Unity Gateway. Older material says AI Gateway. Know both.
27. What do you put on every endpoint? Rate limit per user and per endpoint, usage tracking, inference table, PII guardrail on BLOCK, CAN_QUERY only for the groups that need it.
28. What is an inference table? The payload log, in Unity Catalog, so you can see what was sent and what was blocked.
29. What is a fallback? A second served entity if the first errors or is over its limit. Useful between a foundation model and an in-tenant Azure OpenAI deployment. Not configured live here.
30. Why is the Anthropic template disabled? The prompt would leave the tenant. That is a CISO decision, and the default is no.

## Vector search and Genie

31. Delta Sync versus Direct Vector Access? Delta Sync keeps the index aligned with a Delta table. Direct access is for when you manage the vectors yourself. Delta Sync is the right default for a governed table.
32. Standard versus storage-optimized endpoint? Storage-optimized costs less at large vector counts and has different latency. For a pilot over public PDFs, start standard, measure, then decide.
33. What must a Genie space have before you call it done? Descriptions, certified SQL, sample questions, and a permission set that cannot see PII.
34. Why benchmark Genie before and after? Because "it feels better" is not a result. Fifteen questions, scored, written down.

## Model governance

35. Why UC model registry, not the workspace one? Workspace registry does not travel with the grant model. UC does.
36. What is `@champion`? The alias production traffic uses. Moving it is a privileged action.
37. What does this repo require before promotion? A better metric than the current champion, and a non-empty `approved_by`.
38. What is a model card for? So a reviewer who was not in the room can see owner, data sources, limits, and approval status. Align the sections with SR 11-7 ideas: development, validation, ongoing monitoring. SR 11-7 is public interagency guidance, not a Databricks feature.
39. What did the CPU run actually prove? The entry point runs, the device flag is honored, and the promotion rule works. It did not prove model quality. Accuracy on four rows is a unit test.

## Cost, monitoring, security

40. Where do failed-login queries run? Log Analytics, KQL in `sql/log_analytics_kql.kql`, fed by the diagnostic setting. Not executed against live rows yet.
41. Where do grant-change queries run? `system.access.audit`, once a metastore and system tables exist.
42. Why did metric export fail? The API returned "Metric export is not enabled." Logs were kept. Metrics were dropped. Say that.
43. Why OIDC for GitHub? So CI has no stored Azure secret. The workflow skips plan if the federated credential is not configured. It has not been executed.
44. Why is a 7-day token cap a security control? A stolen token should not be a two-year credential. 730 days was the default I found.
45. What is the blast radius of workspace admin? High. It is break-glass. Day-to-day grants go to groups.
46. What would you revoke first in a compromised-token incident? The token, then the user's sessions, then you read the audit log for what it did. You do not start by rotating unrelated secrets.
47. Why is "no public IP" not "private workspace"? Users and APIs still hit the public control plane. Private Link plus public access disabled is the private workspace. ADR-0003.
48. What did the subscription policy teach you? The cloud's control wins. Terraform that disagrees will fail or, worse, fight the policy on every plan. Match it and document it.
49. What data is in the lab? Public FDIC BankFind failures and institutions, plus Faker rows labeled synthetic. No bank customer data.
50. What will you not claim in the interview? That Unity Catalog is on, that a vector index exists, that a GPU job ran, or that CI is green. The coverage matrix is the list. Anything else is a story I have not earned.
