# Building a governed agent here

The agent is a service principal. It is not you.

It gets:

- USE CATALOG and USE SCHEMA on `prod` and `prod.gold`
- SELECT on the named gold tables (institutions, failures)
- EXECUTE on `lookup_bank`
- SELECT on the vector index
- CAN_QUERY on the serving endpoint

It does not get SELECT on `prod.gold.synthetic_complaints`. A denied query against that table is part of the test, not a failure.

Auth choice:

- Service principal: batch jobs, the published agent, anything that runs when you are asleep.
- On-behalf-of-user: an interactive tool where the user's own grants must apply, so the agent cannot see more than the person who asked.

Every endpoint sits behind Unity Gateway (the current name for what older docs call AI Gateway): a per-user rate limit, payload logging to an inference table, and a PII guardrail set to BLOCK. A prompt with an SSN does not reach the model.

No endpoint is deployed in this lab yet. The configs are in `project-2-genai-rag-ai-gateway/configs/`. Deploying them requires the metastore from ADR-0005.
