"""Apply workspace-level admin settings that Terraform cannot see until the host exists.

Uses the caller's Azure CLI login (Databricks Azure CLI auth). No PAT is created.
Prints status only. Never prints tokens.

Docs checked 2026-10-27:
  https://learn.microsoft.com/en-us/azure/databricks/admin/workspace-settings/
  https://docs.databricks.com/api/workspace/workspaceconf
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import requests

# Regulator-relevant workspace conf keys. Values are the lab posture:
# short-lived tokens, no download of results to local disk where the API allows,
# verbose audit. Keys the API rejects are recorded, not hidden.
WORKSPACE_CONF = {
    "enableTokensConfig": "true",
    "maxTokenLifetimeDays": "7",
    "enableResultsDownloading": "false",
    "storeInteractiveNotebookResultsInCustomerAccount": "true",
    "enableVerboseAuditLogs": "true",
    "enableExportNotebook": "false",
}


def _az_token() -> str:
    completed = subprocess.run(
        [
            "az",
            "account",
            "get-access-token",
            "--resource",
            "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d",
            "--query",
            "accessToken",
            "-o",
            "tsv",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    token = completed.stdout.strip()
    if not token:
        raise RuntimeError("Azure CLI did not return a Databricks access token")
    return token


def _request(method: str, url: str, token: str, body: dict | None = None) -> requests.Response:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.request(method, url, headers=headers, json=body, timeout=60)
    return response


def main() -> int:
    host = os.environ.get("DATABRICKS_HOST", "").rstrip("/")
    if not host:
        print("DATABRICKS_HOST is required", file=sys.stderr)
        return 2
    token = _az_token()
    evidence: dict[str, object] = {"host": host, "attempted": WORKSPACE_CONF, "results": []}

    # Read current conf first so the learning log can show before/after.
    current = _request("GET", f"{host}/api/2.0/workspace-conf?keys={','.join(WORKSPACE_CONF)}", token)
    evidence["before"] = {"status": current.status_code, "body": _safe_json(current)}

    patch = _request("PATCH", f"{host}/api/2.0/workspace-conf", token, WORKSPACE_CONF)
    evidence["patch"] = {"status": patch.status_code, "body": _safe_json(patch)}

    after = _request("GET", f"{host}/api/2.0/workspace-conf?keys={','.join(WORKSPACE_CONF)}", token)
    evidence["after"] = {"status": after.status_code, "body": _safe_json(after)}

    out = Path(__file__).resolve().parents[1] / "evidence" / "workspace-conf.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    print(f"patch status {patch.status_code}")
    return 0 if patch.status_code < 300 else 1


def _safe_json(response: requests.Response) -> object:
    try:
        return response.json()
    except ValueError:
        return {"text": response.text[:500]}


if __name__ == "__main__":
    raise SystemExit(main())
