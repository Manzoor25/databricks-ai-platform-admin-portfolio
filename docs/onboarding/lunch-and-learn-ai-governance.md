# Lunch and learn: AI governance on Databricks (60 minutes)

Audience: analysts, data scientists, and one platform admin. This is a speaker outline, not a recording of a session that was delivered.

## 0–5 min — Why this is an admin problem

Speaker notes: Start with the regulator frame, not the model. A failed bank table from the public FDIC API is fine to demo. A customer table is not. Say out loud that this lab used public FDIC data and synthetic complaints only.

Point: the platform admin decides what is allowed to run, who can query it, and what gets logged. The data scientist does not get to pick a GPU SKU from the marketplace.

## 5–15 min — Identity before features

- Workspace admin is not account admin. Metastore assignment, account groups, and automatic identity management sit in the account console.
- Groups: platform admins, data engineers, data scientists, analysts, AI agents.
- An agent is a service principal with USE CATALOG, USE SCHEMA, SELECT on named tables, and EXECUTE on one function. It does not inherit the user's rights unless you deliberately choose on-behalf-of-user.
- Show `docs/adr/ADR-0005-unity-catalog-account-admin-blocker.md` as the example of stopping at a 403 instead of minting a PAT.

Speaker notes: Ask the room, "Who can create a catalog?" Correct answer: an account admin, or a metastore admin they delegated. A workspace admin cannot invent that right.

## 15–25 min — Compute is a policy, not a menu

- Personal Compute in a new workspace allowed `Standard_NC4as_T4_v3` and a 4320-minute auto-termination default. That is the finding. The override is in `evidence/policy-tightening.json`.
- Persona policies: engineer, scientist CPU, shared. GPU policy exists and is not assigned.
- CPU pool `cpu-lab-pool` has `min_idle_instances = 0`. An idle pool is not a warm VM.
- `enable_gpu = false` changes a JSON definition. It does not start a machine. No GPU job has been run.

Speaker notes: If someone asks for a GPU, ask what the workload is. Prompting a foundation model does not need one. Fine-tuning might. Classic GPU quota in this subscription is zero for the current ML families. Do not request quota in the session.

## 25–40 min — Unity Gateway, not a side door

Current product name (checked 2026-10-27): Unity Gateway. Older decks say AI Gateway.

Walk the template in `project-2-genai-rag-ai-gateway/configs/ai-gateway-rate-limit.json`:

- rate limit per user and per endpoint
- inference table / payload logging
- PII guardrail before the model sees the text
- CAN_QUERY for a named group, not for everyone
- external models referenced as `{{secrets/scope/key}}`, never as a string in git

Speaker notes: Say clearly that this template was not applied. There is no serving endpoint in the lab. Do not demo a live block you did not capture.

## 40–50 min — Genie and model risk

- A Genie space is a governed SQL surface, not a chatbot with the warehouse's full rights. Analysts get the gold tables. They do not get the synthetic PII columns unmasked.
- A model card (`project-2-genai-rag-ai-gateway/MODEL_CARD.md`) is the artifact a model-risk reviewer reads. Development, validation, and ongoing monitoring are the SR 11-7 ideas. This lab filled the card and did not run the validation, because the agent is not deployed.
- Promotion of a classic model requires a better metric and an `approved_by` tag. CPU evidence is `evidence/cpu-train.json`.

Speaker notes: "We wrote 25 questions. We did not score them against a live agent. Saying we did would be the failure mode this talk is about."

## 50–60 min — What you do on Monday

1. Read the coverage matrix before you claim a skill.
2. If Catalog Explorer is empty, file the account-admin request. Do not build a second metastore.
3. Use the persona policy. If the cluster form offers a GPU, stop and tell the platform admin. That is a policy hole, not a feature.
4. Tear down anything you start. Budget is $150. Command is `scripts/teardown.ps1`.

Questions to leave them with:

- What leaves the United States geo if cross-geo processing is on?
- Who can read the inference table, and is that a second copy of the prompt?
- What is the difference between a stopped SQL warehouse and a deleted one?
