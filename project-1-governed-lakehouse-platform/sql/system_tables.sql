-- System table queries a platform admin should be able to run without notes.
-- Docs checked 2026-10-27: https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/

-- 1. Who accessed a tagged PII table in the last 7 days?
SELECT
  event_time,
  user_identity.email AS user_email,
  action_name,
  request_params.full_name_arg AS object_name
FROM system.access.audit
WHERE event_date >= current_date() - INTERVAL 7 DAYS
  AND action_name IN ('getTable', 'commandSubmit')
  AND request_params.full_name_arg LIKE '%synthetic_complaints%'
ORDER BY event_time DESC
LIMIT 100;

-- 2. DBU spend by SKU for this workspace, last 14 days.
SELECT
  usage_date,
  sku_name,
  sum(usage_quantity) AS dbus
FROM system.billing.usage
WHERE usage_date >= current_date() - INTERVAL 14 DAYS
GROUP BY usage_date, sku_name
ORDER BY usage_date DESC, dbus DESC;

-- 3. Lineage: what downstream objects read the failures bronze table?
SELECT
  source_table_full_name,
  target_table_full_name,
  event_date
FROM system.access.table_lineage
WHERE source_table_full_name LIKE '%bank_failures%'
  AND event_date >= current_date() - INTERVAL 30 DAYS
ORDER BY event_date DESC;

-- 4. Grants on the PII table. Alert if a new principal appears.
SELECT
  event_time,
  user_identity.email AS actor,
  action_name,
  request_params
FROM system.access.audit
WHERE action_name IN ('updatePermissions', 'changeSecurableOwner')
  AND event_date >= current_date() - INTERVAL 7 DAYS
ORDER BY event_time DESC;
