# Coverage matrix

Checked 2026-10-27. "Verified" means a command was run and the output is in `evidence/` or in the learning log. "Written, not executed" means the artifact is in the repo and was not run against Databricks, usually because of ADR-0005 (no account admin, no metastore).

| # | Job requirement | Where | Status |
| --- | --- | --- | --- |
| 1 | Expert Databricks administration | `infra/`, `evidence/workspace-conf.json`, ADR-0002, ADR-0005 | Partial. Workspace admin controls verified. Account-level admin blocked on 403. |
| 2 | AI/ML features and best practices | ADR-0001, ADR-0004, Project 2 and 3 configs | Written. Feature names checked against docs on 2026-10-27. |
| 3 | Foundation models, vector search, model governance | `project-2-genai-rag-ai-gateway/configs/`, ADR-0001 | Written, not executed. No metastore, so no index and no endpoint. |
| 4 | Design and implement complex solutions | Three projects plus ADRs | Partial. Azure foundation is deployed. UC-dependent designs are code, not a running system. |
| 5 | Mentorship | `docs/onboarding/`, `docs/LEARNING_LOG.md` | Written. |
| 6 | Strategic roadmap | `docs/roadmap/federal-regulator-12-month.md` | Written. |
| 7 | Govern AI Gateway / Unity Gateway | `project-2-genai-rag-ai-gateway/configs/ai-gateway-rate-limit.json` | Written, not applied. Current product name is Unity Gateway. |
| 8 | Cluster and workspace configuration | `infra/compute.tf`, `evidence/plans/cluster-policies.json`, workspace conf | Policies rendered and validated. Not pushed to the workspace API in this session. Workspace conf verified. |
| 9 | AI-assistive feature toggles and external model keys | `docs/onboarding/ai-feature-matrix.md`, external model templates | Templates only. No API key was created or stored. |
| 10 | Unity Catalog administration | `project-1-governed-lakehouse-platform/sql/governance.sql`, ADR-0005 | Written, not executed. Assignment requires an account admin. |
| 11 | Compute and cost, including GPU governance | ADR-0004, `docs/runbooks/enable-gpu-compute.md`, `enable_gpu = false` | Policy and IaC written and `terraform validate` passed. Execution on CPU (`evidence/cpu-train.json`). No GPU workload was run. GPU-ready by the `device` flag. |
| 12 | Monitoring and logging | Diagnostic setting (imported to state), `sql/log_analytics_kql.kql`, `sql/system_tables.sql` | Diagnostic setting exists. KQL and system-table queries are written, not executed (no rows yet; system tables need a metastore). |
| 13 | Accreditation prep | `docs/certification/study-guide.md` | Written from the public accreditation page, fetched 2026-10-27. |
| 14 | Onboarding and Q&A | `docs/onboarding/faq.md` | Written. |

GPU line, as required: Policy and IaC built and validated; execution on CPU due to quota and because AI Runtime was not attached in this session; GPU-ready by parameter flag.
