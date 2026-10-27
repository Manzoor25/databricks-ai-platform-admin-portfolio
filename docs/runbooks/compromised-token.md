# Runbook: compromised token

1. Revoke the token in the workspace admin console, or with the token API if you are the owner. Do this before you investigate.
2. If the token belonged to a service principal, disable the service principal in Entra ID. A Databricks-side revoke is not enough if the secret is still valid.
3. Read `system.access.audit` and the Log Analytics `accounts` category for that identity from an hour before the report.
4. Rotate anything the token could have read from Key Vault. Assume it read it.
5. Confirm `maxTokenLifetimeDays` is still 7. If someone raised it, that is part of the incident.
6. Write down what the token actually did. Do not write down what it could have done and present it as fact.
