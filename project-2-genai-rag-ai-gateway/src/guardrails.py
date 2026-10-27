"""Local stand-in for the AI Gateway PII guardrail.

The serving endpoint guardrail is the control that blocks a request in
Databricks. This function is the same rule, testable without an endpoint:
if the prompt contains an SSN-shaped string, block it and do not call a model.
"""

from __future__ import annotations

import re

SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def screen_prompt(prompt: str) -> dict[str, object]:
    hits: list[str] = []
    if SSN.search(prompt):
        hits.append("ssn")
    if EMAIL.search(prompt):
        hits.append("email")
    return {"allowed": not hits, "blocked_types": hits}
