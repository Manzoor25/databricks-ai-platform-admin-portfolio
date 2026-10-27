# ADR-0003: Secure cluster connectivity now, Private Link behind a flag

- Status: Accepted
- Date: 2026-10-27

## Context

A federal financial regulator typically wants:

- no public IPs on compute nodes,
- no public path to the workspace UI and APIs,
- private access to ADLS and Key Vault,
- and a written exception if any of those are deferred.

Private endpoints and a disabled public front end add cost (Private Link, DNS zones, and often a jump host or VPN) and block this lab's CLI from the laptop unless a private path exists.

## Decision

- Ship **VNet injection + secure cluster connectivity** (`no_public_ip = true`) now. Cluster nodes have no public IP.
- Keep **front-end Private Link and public network access disabled** behind `enable_private_link` (default `false`).
- Keep storage and Key Vault private endpoints in the same flag. When the flag is on, Key Vault public network access is turned off.

## When a regulator would require the flag on

Turn it on before any non-public data lands in the workspace, or before an authorization boundary (FedRAMP / agency ATO) is claimed. The trigger is data classification, not user count. Public FDIC data and synthetic PII in a personal lab do not meet that trigger. Customer bank data would.

## Consequences

- Do not describe this lab as a private workspace. Say: "data plane is VNet-injected with SCC; control plane is still public, by an explicit cost decision recorded in ADR-0003."
- The Terraform already contains the private endpoint resource. Flipping the flag is a plan/apply, not a redesign.
