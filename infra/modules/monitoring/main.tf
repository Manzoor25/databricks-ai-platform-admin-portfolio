variable "name_prefix" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "tags" { type = map(string) }
variable "alert_email" { type = string }
variable "monthly_budget_usd" { type = number }

data "azurerm_subscription" "current" {}

resource "azurerm_log_analytics_workspace" "this" {
  name                = "log-${var.name_prefix}"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = var.tags
}

resource "azurerm_monitor_action_group" "budget" {
  name                = "ag-${var.name_prefix}-budget"
  resource_group_name = var.resource_group_name
  short_name          = "dbxbudget"
  tags                = var.tags

  email_receiver {
    name                    = "owner"
    email_address           = var.alert_email
    use_common_alert_schema = true
  }
}

resource "azurerm_consumption_budget_subscription" "this" {
  name            = "budget-${var.name_prefix}"
  subscription_id = data.azurerm_subscription.current.id
  amount          = var.monthly_budget_usd
  time_grain      = "Monthly"

  # Azure requires the budget start to be the first day of the current or a
  # future month, at midnight UTC. plantimestamp() is stable across plans.
  time_period {
    start_date = "${formatdate("YYYY-MM-01", plantimestamp())}T00:00:00Z"
  }

  filter {
    dimension {
      name   = "ResourceGroupName"
      values = [var.resource_group_name]
    }
  }

  notification {
    enabled        = true
    threshold      = 50
    operator       = "GreaterThanOrEqualTo"
    threshold_type = "Actual"
    contact_emails = [var.alert_email]
  }

  notification {
    enabled        = true
    threshold      = 80
    operator       = "GreaterThanOrEqualTo"
    threshold_type = "Actual"
    contact_emails = [var.alert_email]
  }

  notification {
    enabled        = true
    threshold      = 100
    operator       = "GreaterThanOrEqualTo"
    threshold_type = "Actual"
    contact_emails = [var.alert_email]
  }

  lifecycle {
    ignore_changes = [time_period]
  }
}

output "log_analytics_id" { value = azurerm_log_analytics_workspace.this.id }
output "log_analytics_name" { value = azurerm_log_analytics_workspace.this.name }
output "action_group_id" { value = azurerm_monitor_action_group.budget.id }
output "budget_name" { value = azurerm_consumption_budget_subscription.this.name }
