output "resource_group_name" {
  value = azurerm_resource_group.this.name
}

output "workspace_url" {
  value = module.workspace.workspace_url
}

output "workspace_id" {
  value = module.workspace.workspace_id
}

output "storage_account_name" {
  value = module.storage.storage_account_name
}

output "key_vault_name" {
  value = module.keyvault.key_vault_name
}

output "key_vault_uri" {
  value = module.keyvault.key_vault_uri
}

output "log_analytics_workspace_id" {
  value = module.monitoring.log_analytics_id
}

output "budget_name" {
  value = module.monitoring.budget_name
}

output "enable_gpu" {
  value = var.enable_gpu
}

output "enable_private_link" {
  value = var.enable_private_link
}
