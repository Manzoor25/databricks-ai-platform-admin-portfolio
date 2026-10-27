"""Create workspace groups and a CPU pool. Does not start a VM or a GPU pool.

Workspace groups are local SCIM groups. They are not account-level Entra sync.
That sync needs an account admin (ADR-0005). The CPU pool is created with
min_idle_instances=0 so the pool object exists and no node is warmed.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import requests

HOST = os.environ["DATABRICKS_HOST"].rstrip("/")
TENANT = "16b3c013-d300-468d-ac64-7eda0820b6d3"
SUBSCRIPTION = "0076286c-b9d6-4cc4-9617-774b869e75e2"
RG = "rg-dbx-ai-admin-lab"
REPO = "Manzoor25/databricks-ai-platform-admin-portfolio"
APP_NAME = "dbx-ai-admin-lab-gha"
USER_OBJECT_ID = "412a77b8-af05-4138-8760-ba5dd2af9b4b"

GROUPS = {
    "dbx-platform-admins": "b4cd860b-3cc3-48b9-84d9-37c1f8807640",
    "dbx-data-engineers": "28d0f22d-0522-4d81-91bc-0b6bffe24280",
    "dbx-data-scientists": "f8f6c33e-d3fd-4ec4-aae4-4610c2f98e19",
    "dbx-analysts": "44f6855d-cbc9-41f3-9c0f-eadb83b18489",
    "dbx-ai-agents": "e8a5c5c8-e242-44f4-9f2e-018060419d73",
}

POLICY_GRANTS = {
    "001FB22F6D18074A": "dbx-data-engineers",
    "001A994CD1E24E23": "dbx-data-scientists",
    "001E1DD5311C19C2": "dbx-analysts",
}


def az(*args: str) -> subprocess.CompletedProcess[str]:
    executable = "az.cmd" if os.name == "nt" else "az"
    return subprocess.run(
        [executable, *args],
        check=False,
        capture_output=True,
        text=True,
    )


def token() -> str:
    completed = az(
        "account",
        "get-access-token",
        "--resource",
        "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d",
        "--tenant",
        TENANT,
        "--query",
        "accessToken",
        "-o",
        "tsv",
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr[-400:])
    return completed.stdout.strip()


def api(method: str, path: str, bearer: str, **kwargs: object) -> requests.Response:
    return requests.request(
        method,
        f"{HOST}{path}",
        headers={"Authorization": f"Bearer {bearer}", "Content-Type": "application/json"},
        timeout=60,
        **kwargs,
    )


def ensure_groups(bearer: str) -> list[dict]:
    listed = api("GET", "/api/2.0/preview/scim/v2/Groups?count=100", bearer)
    existing = {
        item.get("displayName"): item.get("id")
        for item in listed.json().get("Resources", [])
    }
    results = []
    for name, entra_id in GROUPS.items():
        if name in existing:
            results.append({"name": name, "id": existing[name], "action": "exists"})
            continue
        created = api(
            "POST",
            "/api/2.0/preview/scim/v2/Groups",
            bearer,
            json={
                "displayName": name,
                "externalId": entra_id,
                "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
            },
        )
        body = created.json() if created.content else {}
        results.append(
            {
                "name": name,
                "status": created.status_code,
                "id": body.get("id"),
                "action": "created" if created.status_code in (200, 201) else "failed",
                "detail": created.text[:300] if created.status_code >= 300 else "",
            }
        )
    return results


def add_self_to_platform_admins(bearer: str) -> dict:
    me = api("GET", "/api/2.0/preview/scim/v2/Me", bearer)
    user_id = me.json().get("id")
    groups = api(
        "GET",
        "/api/2.0/preview/scim/v2/Groups?filter=displayName%20eq%20dbx-platform-admins",
        bearer,
    )
    resources = groups.json().get("Resources", [])
    if not resources or not user_id:
        return {"status": "skipped", "me": me.status_code, "groups": groups.status_code}
    group_id = resources[0]["id"]
    patched = api(
        "PATCH",
        f"/api/2.0/preview/scim/v2/Groups/{group_id}",
        bearer,
        json={
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
            "Operations": [
                {"op": "add", "path": "members", "value": [{"value": user_id}]}
            ],
        },
    )
    return {"status": patched.status_code, "workspace_user_id": user_id, "group_id": group_id}


def ensure_cpu_pool(bearer: str) -> dict:
    listed = api("GET", "/api/2.0/instance-pools/list", bearer)
    pools = listed.json().get("instance_pools", []) if listed.ok else []
    for pool in pools:
        if pool.get("instance_pool_name") == "cpu-lab-pool":
            return {
                "action": "exists",
                "instance_pool_id": pool.get("instance_pool_id"),
                "min_idle_instances": pool.get("min_idle_instances"),
                "stats": pool.get("stats"),
            }
    created = api(
        "POST",
        "/api/2.0/instance-pools/create",
        bearer,
        json={
            "instance_pool_name": "cpu-lab-pool",
            "node_type_id": "Standard_DS3_v2",
            "min_idle_instances": 0,
            "max_capacity": 1,
            "idle_instance_autotermination_minutes": 10,
        },
    )
    body = created.json() if created.content else {}
    return {
        "action": "created" if created.ok else "failed",
        "status": created.status_code,
        "instance_pool_id": body.get("instance_pool_id"),
        "min_idle_instances": 0,
        "detail": created.text[:400] if not created.ok else "",
    }


def grant_policies(bearer: str) -> list[dict]:
    results = []
    for policy_id, group_name in POLICY_GRANTS.items():
        current = api("GET", f"/api/2.0/permissions/cluster-policies/{policy_id}", bearer)
        acl = current.json().get("access_control_list", []) if current.ok else []
        if any(item.get("group_name") == group_name for item in acl):
            results.append({"policy_id": policy_id, "group": group_name, "action": "exists"})
            continue
        updated = api(
            "PATCH",
            f"/api/2.0/permissions/cluster-policies/{policy_id}",
            bearer,
            json={
                "access_control_list": [
                    {"group_name": group_name, "permission_level": "CAN_USE"}
                ]
            },
        )
        results.append(
            {
                "policy_id": policy_id,
                "group": group_name,
                "status": updated.status_code,
                "action": "granted" if updated.ok else "failed",
                "detail": updated.text[:240] if not updated.ok else "",
            }
        )
    return results


def entra_member() -> dict:
    completed = az(
        "ad",
        "group",
        "member",
        "add",
        "--group",
        GROUPS["dbx-platform-admins"],
        "--member-id",
        USER_OBJECT_ID,
    )
    text = (completed.stdout + completed.stderr)[-300:]
    already = "already exist" in text.lower()
    return {
        "status": completed.returncode,
        "action": "exists" if already else ("added" if completed.returncode == 0 else "failed"),
        "detail": "" if completed.returncode == 0 or already else text,
    }


def oidc_app() -> dict:
    listed = az("ad", "app", "list", "--display-name", APP_NAME, "--query", "[].appId", "-o", "tsv")
    app_id = listed.stdout.strip().splitlines()[0] if listed.stdout.strip() else ""
    created = False
    if not app_id:
        made = az(
            "ad",
            "app",
            "create",
            "--display-name",
            APP_NAME,
            "--sign-in-audience",
            "AzureADMyOrg",
            "--query",
            "appId",
            "-o",
            "tsv",
        )
        if made.returncode != 0:
            return {"action": "failed", "detail": made.stderr[-400:]}
        app_id = made.stdout.strip()
        created = True
    sp = az("ad", "sp", "create", "--id", app_id)
    sp_text = (sp.stdout + sp.stderr)[-240:]
    cred_path = Path(__file__).resolve().parent / "_federated-credential.json"
    cred_path.write_text(
        json.dumps(
            {
                "name": "github-main",
                "issuer": "https://token.actions.githubusercontent.com",
                "subject": f"repo:{REPO}:ref:refs/heads/main",
                "audiences": ["api://AzureADTokenExchange"],
                "description": "GitHub Actions plan on main. No client secret.",
            }
        ),
        encoding="utf-8",
    )
    fed = az(
        "ad",
        "app",
        "federated-credential",
        "create",
        "--id",
        app_id,
        "--parameters",
        str(cred_path),
    )
    cred_path.write_text(
        json.dumps(
            {
                "name": "github-pull-request",
                "issuer": "https://token.actions.githubusercontent.com",
                "subject": f"repo:{REPO}:pull_request",
                "audiences": ["api://AzureADTokenExchange"],
                "description": "GitHub Actions plan on pull requests. No client secret.",
            }
        ),
        encoding="utf-8",
    )
    fed_pr = az(
        "ad",
        "app",
        "federated-credential",
        "create",
        "--id",
        app_id,
        "--parameters",
        str(cred_path),
    )
    cred_path.unlink(missing_ok=True)
    scope = f"/subscriptions/{SUBSCRIPTION}/resourceGroups/{RG}"
    role = az(
        "role",
        "assignment",
        "create",
        "--assignee",
        app_id,
        "--role",
        "Reader",
        "--scope",
        scope,
    )
    fed_text = (fed.stdout + fed.stderr)[-240:]
    fed_pr_text = (fed_pr.stdout + fed_pr.stderr)[-240:]
    return {
        "action": "created" if created else "exists",
        "app_id": app_id,
        "client_secret_created": False,
        "service_principal": "ok" if sp.returncode == 0 or "already" in sp_text.lower() else sp_text,
        "federated_credential": "ok"
        if fed.returncode == 0 or "already" in fed_text.lower()
        else fed_text,
        "federated_credential_pr": "ok"
        if fed_pr.returncode == 0 or "already" in fed_pr_text.lower()
        else fed_pr_text,
        "role": "Reader",
        "scope": scope,
        "role_assignment": "ok" if role.returncode == 0 else (role.stderr or role.stdout)[-240:],
    }


def main() -> None:
    bearer = token()
    evidence = {
        "workspace_groups": ensure_groups(bearer),
        "platform_admin_membership": add_self_to_platform_admins(bearer),
        "entra_platform_admin_membership": entra_member(),
        "cpu_pool": ensure_cpu_pool(bearer),
        "policy_grants": grant_policies(bearer),
        "github_oidc_app": oidc_app(),
        "gpu_pool": "not created",
        "note": "CPU pool min_idle_instances is 0. No cluster was started. No GPU pool was created.",
    }
    out = Path(__file__).resolve().parents[1] / "evidence" / "identity-and-pool.json"
    out.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
