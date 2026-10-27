variable "name_prefix" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "tags" { type = map(string) }
variable "vnet_id" { type = string }
variable "public_subnet_name" { type = string }
variable "private_subnet_name" { type = string }
variable "public_subnet_nsg_assoc_id" { type = string }
variable "private_subnet_nsg_assoc_id" { type = string }
variable "log_analytics_workspace_id" { type = string }
variable "enable_private_link" { type = bool }

resource "azurerm_databricks_workspace" "this" {
  name                                  = "dbw-${var.name_prefix}"
  resource_group_name                   = var.resource_group_name
  location                              = var.location
  sku                                   = "premium"
  managed_resource_group_name           = "rg-${var.name_prefix}-dbx-managed"
  public_network_access_enabled         = var.enable_private_link ? false : true
  network_security_group_rules_required = "NoAzureDatabricksRules"
  tags                                  = var.tags

  custom_parameters {
    no_public_ip                                         = true
    virtual_network_id                                   = var.vnet_id
    public_subnet_name                                   = var.public_subnet_name
    private_subnet_name                                  = var.private_subnet_name
    public_subnet_network_security_group_association_id  = var.public_subnet_nsg_assoc_id
    private_subnet_network_security_group_association_id = var.private_subnet_nsg_assoc_id
    storage_account_sku_name                             = "Standard_LRS"
  }

  depends_on = [
    var.public_subnet_nsg_assoc_id,
    var.private_subnet_nsg_assoc_id,
  ]
}

resource "azurerm_monitor_diagnostic_setting" "workspace" {
  name                       = "diag-${var.name_prefix}-dbw"
  target_resource_id         = azurerm_databricks_workspace.this.id
  log_analytics_workspace_id = var.log_analytics_workspace_id

  enabled_log {
    category = "accounts"
  }
  enabled_log {
    category = "clusters"
  }
  enabled_log {
    category = "dbfs"
  }
  enabled_log {
    category = "jobs"
  }
  enabled_log {
    category = "notebook"
  }
  enabled_log {
    category = "sqlPermissions"
  }
  enabled_log {
    category = "workspace"
  }
  enabled_log {
    category = "unityCatalog"
  }

  # Databricks workspaces in this subscription return
  # "Metric export is not enabled" if AllMetrics is requested.
  # Logs are the control that matters for the three KQL queries.
}

output "workspace_id" { value = azurerm_databricks_workspace.this.workspace_id }
output "workspace_url" { value = "https://${azurerm_databricks_workspace.this.workspace_url}" }
output "workspace_resource_id" { value = azurerm_databricks_workspace.this.id }
output "managed_resource_group_id" { value = azurerm_databricks_workspace.this.managed_resource_group_id }
