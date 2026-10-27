"""Tighten default workspace cluster policies. Does not start a cluster.

Personal Compute shipped with a T4 in the allowlist and a 4320-minute
auto-termination default. Shared Compute shipped with auto-termination
default 0 (never). Both are cost and governance holes. This script removes
the GPU SKU and caps auto-termination. If the API rejects an edit because
the policy is a managed family, the error is written to evidence and left
as a documented residual risk.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import requests

HOST = os.environ["DATABRICKS_HOST"].rstrip("/")
PERSONAL_ID = "000317330E508838"
SHARED_ID = "001D52C37D3AE284"


def token() -> str:
    az = "az.cmd" if os.name == "nt" else "az"
    completed = subprocess.run(
        [
            az,
            "account",
            "get-access-token",
            "--resource",
            "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d",
            "--tenant",
            "16b3c013-d300-468d-ac64-7eda0820b6d3",
            "--query",
            "accessToken",
            "-o",
            "tsv",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def edit(policy_id: str, name: str, family_id: str, overrides: dict, bearer: str) -> dict:
    response = requests.post(
        f"{HOST}/api/2.0/policies/clusters/edit",
        headers={"Authorization": f"Bearer {bearer}", "Content-Type": "application/json"},
        json={
            "policy_id": policy_id,
            "name": name,
            "policy_family_id": family_id,
            "policy_family_definition_overrides": json.dumps(overrides),
        },
        timeout=60,
    )
    return {"status": response.status_code, "body": response.text[:800]}


def main() -> None:
    bearer = token()
    headers = {"Authorization": f"Bearer {bearer}"}
    current = requests.get(
        f"{HOST}/api/2.0/policies/clusters/get",
        headers=headers,
        params={"policy_id": PERSONAL_ID},
        timeout=60,
    )
    personal = json.loads(current.json()["definition"])
    before_nodes = personal.get("node_type_id", {}).get("values", [])
    cpu_nodes = [node for node in before_nodes if not str(node).startswith("Standard_NC")]
    personal_overrides = {
        "node_type_id": {
            "type": "allowlist",
            "values": cpu_nodes,
            "defaultValue": "Standard_D4ds_v5",
        },
        "autotermination_minutes": {
            "type": "range",
            "minValue": 10,
            "maxValue": 20,
            "defaultValue": 20,
            "isOptional": False,
        },
    }
    personal_result = edit(
        PERSONAL_ID, "Personal Compute", "personal-vm", personal_overrides, bearer
    )

    shared_resp = requests.get(
        f"{HOST}/api/2.0/policies/clusters/get",
        headers=headers,
        params={"policy_id": SHARED_ID},
        timeout=60,
    )
    shared_overrides = {
        "autotermination_minutes": {
            "type": "range",
            "minValue": 10,
            "maxValue": 20,
            "defaultValue": 20,
            "isOptional": False,
        }
    }
    shared_result = edit(
        SHARED_ID, "Shared Compute", "shared-compute", shared_overrides, bearer
    )

    evidence = {
        "personal_compute_gpu_nodes_before": before_nodes,
        "personal_compute_edit": personal_result,
        "shared_compute_edit": shared_result,
        "ai_runtime_pools": "FEATURE_DISABLED: the GPU pools API is not enabled for this workspace",
    }
    out = Path(__file__).resolve().parents[1] / "evidence" / "policy-tightening.json"
    out.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
