# AI feature enablement decision matrix

For a US financial regulator. Cross-geo processing stays off. United States geo already lists the features this lab cares about as Available (Designated Services, checked 2026-10-26), so turning cross-geo on would expand data processing for no benefit.

| Feature | Data that leaves the table | Risk | Recommended setting | Approver |
| --- | --- | --- | --- | --- |
| Databricks Assistant / Genie Code | Code and a sample of cell context, processed in-geo | Low for public data, high if a notebook holds non-public data | On for this lab. Off in any workspace that holds confidential data until the processing terms are reviewed | Platform admin + privacy |
| Partner-powered AI features | Depends on the partner. Treat as a third-party processor | High | Off until a named partner and a DPA exist | CISO |
| Genie | Table and column metadata, query text, sampled values if the space allows it | Medium. Sampling is the sharp edge | On for gold tables that are public. Off for any table tagged `pii=true` | Data owner |
| AI Functions (`ai_query`, `ai_classify`) | The column values you pass in | Medium. Easy to point at the wrong column | On, bound to a Unity Gateway endpoint with PII block | Platform admin |
| Foundation Model APIs, pay-per-token | The prompt and retrieved chunks | Medium. Stay in-geo | On for the pilot. No cross-geo | Model risk lead |
| External model (Azure OpenAI in-tenant) | Prompt leaves Databricks but stays in the tenant | Medium, acceptable with a secret scope and no key in git | Template ready. Not deployed | Platform admin |
| External model (Anthropic, OpenAI public) | Prompt leaves the tenant | High | Disabled. Templates in repo, `enabled: false` | CISO, and the answer is still no by default |
| AI Runtime serverless GPU | Training data is processed by Databricks-managed GPU in-geo | Medium. Cost, not residency | Probe only. Not used in this run | Platform admin |
| Serverless SQL | Query text and results in the Databricks control plane, in-geo | Low | On, auto-stop, tagged | Platform admin |

Workspace state captured 2026-10-27 is in `evidence/workspace-conf.json`. That file is token and export policy, not the Assistant toggle. The Assistant and Genie toggles are account or workspace preview settings this user could not read without account admin. Do not invent a before/after for them.
