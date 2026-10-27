# Runbook: cluster will not start

1. Read the cluster event log. The first error is the one you chase.
2. Policy denial: node type, runtime, or missing tag. Do not widen the policy to make one user happy.
3. Quota: `az vm list-usage --location eastus`. A GPU denial with family limit 0 is expected. Send them to `enable-gpu-compute.md`.
4. Network: this workspace is VNet-injected. If the subnet has no free IPs, that is the error. Do not recreate the workspace.
5. If the event says the workspace is unreachable, check whether someone disabled public network access. This lab did not. ADR-0003 says the control plane is still public on purpose.
