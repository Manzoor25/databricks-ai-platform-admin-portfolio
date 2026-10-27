# Model card — regulatory assistant (not deployed)

Status: **template filled for review. The agent was not registered, not served, and not evaluated against a live endpoint.** Do not cite this card as evidence of a validation test.

Aligned with the public ideas in SR 11-7 (development, validation, ongoing monitoring). This lab is not a federal model-risk exam and not an FDIC system.

| Field | Value |
| --- | --- |
| Model name | `prod.ai.regulatory_assistant` (intended UC name; catalog does not exist) |
| Version | none |
| Aliases | `@champion` / `@challenger` designed, not set |
| Owner | platform admin lab |
| Risk tier | would be Moderate if deployed on public guidance only; not approved |
| Approval status | not submitted |
| Data sources | public FDIC BankFind failures and institutions; public FDIC guidance pages if a future ingest respects robots.txt; synthetic complaints labeled `synthetic-faker` |
| Data that must never be included | non-public exam data, customer PII, credentials |
| Intended use | answer questions about public bank-failure facts, with a tool call for `lookup_bank` |
| Out of scope | credit decisions, enforcement recommendations, anything a human examiner would sign |
| Foundation model | pay-per-token, United States geo, cross-geo off. Not selected as a deployed endpoint |
| External models | Azure OpenAI template only. Anthropic and OpenAI templates are `enabled: false` |
| GPU | not used. Not required for this design |

## Development

The design is a tool-calling RAG agent over chunked public documents, traced with MLflow, registered in Unity Catalog, and served on CPU with scale-to-zero. Chunking and the SSN-shaped guardrail have unit tests. The serving endpoint was not created (ADR-0005).

## Validation

`eval/regulatory_assistant_eval.jsonl` has 25 questions written from public facts. **They have not been scored.** There is no correctness, groundedness, relevance, or safety number to report. A future run must use an LLM judge plus a human review on a sample, and must fail closed if the judge cannot cite a retrieved chunk.

## Ongoing monitoring

Designed, not enabled: inference table, Unity Gateway usage tracking, rate-limit denials, and a drift check on the classic distress model (separate from this agent). No dashboard is live.

## Change control

A new alias promotion requires a better eval than the current champion and a named `approved_by`. Neither alias exists today.
