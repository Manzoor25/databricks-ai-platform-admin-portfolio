# Classic compute governance is applied by the Databricks workspace provider
# after the workspace exists. These resources are in compute_workspace.tf and
# are created by scripts/configure_workspace.py using the workspace API, because
# the Terraform workspace provider needs a live host that does not exist at
# the first plan. The definitions below are the source of truth for policies
# and are also rendered as JSON for the API script and for plan evidence.

locals {
  cluster_policy_common = {
    "spark_version" = {
      type         = "unlimited"
      defaultValue = "auto:latest-lts"
    }
    "autotermination_minutes" = {
      type   = "fixed"
      value  = 20
      hidden = true
    }
    "custom_tags.project" = {
      type  = "fixed"
      value = var.project
    }
    "custom_tags.owner" = {
      type  = "fixed"
      value = var.owner
    }
    "custom_tags.cost-center" = {
      type  = "fixed"
      value = var.cost_center
    }
    "custom_tags.environment" = {
      type  = "fixed"
      value = var.environment
    }
  }

  policy_data_engineer = merge(local.cluster_policy_common, {
    "node_type_id" = {
      type         = "allowlist"
      values       = ["Standard_D4s_v5", "Standard_D8s_v5"]
      defaultValue = "Standard_D4s_v5"
    }
    "autoscale.min_workers" = { type = "fixed", value = 1 }
    "autoscale.max_workers" = { type = "range", minValue = 1, maxValue = 4, defaultValue = 2 }
    "dbus_per_hour"         = { type = "range", maxValue = 15 }
  })

  policy_data_scientist_cpu = merge(local.cluster_policy_common, {
    "spark_version" = {
      type         = "regex"
      pattern      = ".*-ml-.*"
      defaultValue = "auto:latest-ml"
    }
    "node_type_id" = {
      type         = "allowlist"
      values       = ["Standard_D4s_v5", "Standard_D8s_v5"]
      defaultValue = "Standard_D4s_v5"
    }
    "num_workers"        = { type = "fixed", value = 0, hidden = true }
    "data_security_mode" = { type = "fixed", value = "SINGLE_USER" }
    "dbus_per_hour"      = { type = "range", maxValue = 8 }
  })

  # GPU policy is always defined. It is not assigned to any persona unless
  # enable_gpu = true. Applying this policy does not start a VM.
  policy_data_scientist_gpu = merge(local.cluster_policy_common, {
    "spark_version" = {
      type         = "regex"
      pattern      = ".*-ml-.*"
      defaultValue = "auto:latest-ml"
    }
    "node_type_id" = {
      type = "allowlist"
      values = [
        "Standard_NC4as_T4_v3",
        "Standard_NC8as_T4_v3",
        "Standard_NC24ads_A100_v4",
      ]
    }
    "num_workers"             = { type = "fixed", value = 0, hidden = true }
    "autotermination_minutes" = { type = "fixed", value = 15, hidden = true }
    "dbus_per_hour"           = { type = "range", maxValue = 20 }
    "custom_tags.workload"    = { type = "fixed", value = "gpu-training" }
  })

  policy_shared = merge(local.cluster_policy_common, {
    "node_type_id" = {
      type         = "allowlist"
      values       = ["Standard_D4s_v5"]
      defaultValue = "Standard_D4s_v5"
    }
    "data_security_mode"    = { type = "fixed", value = "USER_ISOLATION" }
    "autoscale.max_workers" = { type = "range", maxValue = 2, defaultValue = 1 }
    "dbus_per_hour"         = { type = "range", maxValue = 8 }
  })
}

# Definition only. count is always 1 so the spec is reviewable with the flag off.
# create_in_workspace flips with enable_gpu. This resource is a local file, not a
# Databricks instance pool and not an Azure VM. Do not read a plan diff here as
# "a GPU machine will start."
resource "local_file" "gpu_pool_definition" {
  filename = "${path.module}/../evidence/plans/gpu-pool-definition.json"
  content = jsonencode({
    instance_pool_name                    = "gpu-lab-pool-definition-only"
    node_type_id                          = "Standard_NC4as_T4_v3"
    min_idle_instances                    = 0
    max_capacity                          = 1
    idle_instance_autotermination_minutes = 10
    create_in_workspace                   = var.enable_gpu
    note                                  = "Not a live pool. enable_gpu only changes this JSON. No databricks_instance_pool resource is declared, so terraform apply cannot start a GPU VM."
  })
}

resource "local_file" "cluster_policies" {
  filename = "${path.module}/../evidence/plans/cluster-policies.json"
  content = jsonencode({
    data_engineer      = local.policy_data_engineer
    data_scientist_cpu = local.policy_data_scientist_cpu
    data_scientist_gpu = local.policy_data_scientist_gpu
    shared_standard    = local.policy_shared
    enable_gpu         = var.enable_gpu
    gpu_pool_live      = false
  })
}
