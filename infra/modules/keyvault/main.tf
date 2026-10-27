variable "name_prefix" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "tags" { type = map(string) }
variable "tenant_id" { type = string }
variable "current_object_id" { type = string }
variable "enable_private_link" { type = bool }
variable "private_endpoint_subnet_id" { type = string }

resource "random_string" "suffix" {
  length  = 4
  upper   = false
  special = false
}

resource "azurerm_key_vault" "this" {
  name                       = "kv-${substr(replace(var.name_prefix, "-", ""), 0, 12)}-${random_string.suffix.result}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  tenant_id                  = var.tenant_id
  sku_name                   = "standard"
  rbac_authorization_enabled = true
  purge_protection_enabled   = false
  soft_delete_retention_days = 7
  # This subscription denies public network access on Key Vault (policy).
  # Keep it off so Terraform does not fight the policy on every apply.
  # Laptop access uses the caller's existing network path or a private endpoint
  # when enable_private_link is true. See ADR-0003.
  public_network_access_enabled = false
  tags                          = var.tags
}

resource "azurerm_role_assignment" "current_secrets_officer" {
  scope                = azurerm_key_vault.this.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = var.current_object_id
}

resource "azurerm_private_endpoint" "kv" {
  count               = var.enable_private_link ? 1 : 0
  name                = "pe-${var.name_prefix}-kv"
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.private_endpoint_subnet_id
  tags                = var.tags

  private_service_connection {
    name                           = "kv"
    private_connection_resource_id = azurerm_key_vault.this.id
    subresource_names              = ["vault"]
    is_manual_connection           = false
  }
}

output "key_vault_id" { value = azurerm_key_vault.this.id }
output "key_vault_name" { value = azurerm_key_vault.this.name }
output "key_vault_uri" { value = azurerm_key_vault.this.vault_uri }
