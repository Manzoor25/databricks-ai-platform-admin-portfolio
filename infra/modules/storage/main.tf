variable "name_prefix" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "tags" { type = map(string) }

resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}

resource "azurerm_storage_account" "uc" {
  name                            = "st${replace(var.name_prefix, "-", "")}${random_string.suffix.result}"
  resource_group_name             = var.resource_group_name
  location                        = var.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  account_kind                    = "StorageV2"
  is_hns_enabled                  = true
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = false
  # Subscription policy denies key-based auth. The AzureRM provider must use
  # Entra ID when it polls the data plane, or container creation returns 403.
  https_traffic_only_enabled    = true
  public_network_access_enabled = false
  tags                          = var.tags

  blob_properties {
    delete_retention_policy {
      days = 7
    }
  }
}

resource "azurerm_storage_container" "uc" {
  name                  = "unity-catalog"
  storage_account_id    = azurerm_storage_account.uc.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_id    = azurerm_storage_account.uc.id
  container_access_type = "private"
}

resource "azurerm_storage_container" "documents" {
  name                  = "regulatory-documents"
  storage_account_id    = azurerm_storage_account.uc.id
  container_access_type = "private"
}

output "storage_account_id" { value = azurerm_storage_account.uc.id }
output "storage_account_name" { value = azurerm_storage_account.uc.name }
output "primary_dfs_endpoint" { value = azurerm_storage_account.uc.primary_dfs_endpoint }
output "uc_container_id" { value = azurerm_storage_container.uc.id }
