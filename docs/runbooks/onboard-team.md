# Runbook: onboard a team

1. Create or confirm the Entra group (`dbx-data-engineers`, `dbx-data-scientists`, `dbx-analysts`). Do not add individuals to workspace grants.
2. Confirm automatic identity management is on. If it is not, you need an account admin. Do not stand up a one-off SCIM connector to avoid that conversation.
3. Grant the group from the matrix in ADR-0002. Analysts get Genie and gold SELECT, not cluster create.
4. Assign the persona cluster policy. Do not give unrestricted cluster create.
5. Send the matching day-1 doc in `docs/onboarding/`.
6. Check the next day that the user can run the one query they were promised, and cannot select the PII table in clear text.
