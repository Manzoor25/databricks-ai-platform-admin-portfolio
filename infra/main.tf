resource "azurerm_resource_group" "this" {
  name     = "rg-${local.name_prefix}"
  location = var.location
  tags     = local.common_tags
}

module "monitoring" {
  source              = "./modules/monitoring"
  name_prefix         = local.name_prefix
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
  tags                = local.common_tags
  alert_email         = var.alert_email
  monthly_budget_usd  = var.monthly_budget_usd
}

module "network" {
  source              = "./modules/network"
  name_prefix         = local.name_prefix
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
  tags                = local.common_tags
  vnet_address_space  = var.vnet_address_space
  public_subnet_cidr  = var.public_subnet_cidr
  private_subnet_cidr = var.private_subnet_cidr
}

module "storage" {
  source              = "./modules/storage"
  name_prefix         = local.name_prefix
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
  tags                = local.common_tags
}

module "keyvault" {
  source                     = "./modules/keyvault"
  name_prefix                = local.name_prefix
  location                   = var.location
  resource_group_name        = azurerm_resource_group.this.name
  tags                       = local.common_tags
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  current_object_id          = data.azurerm_client_config.current.object_id
  enable_private_link        = var.enable_private_link
  private_endpoint_subnet_id = module.network.pe_subnet_id
}

module "workspace" {
  source                      = "./modules/databricks-workspace"
  name_prefix                 = local.name_prefix
  location                    = var.location
  resource_group_name         = azurerm_resource_group.this.name
  tags                        = local.common_tags
  vnet_id                     = module.network.vnet_id
  public_subnet_name          = module.network.public_subnet_name
  private_subnet_name         = module.network.private_subnet_name
  public_subnet_nsg_assoc_id  = module.network.public_nsg_assoc_id
  private_subnet_nsg_assoc_id = module.network.private_nsg_assoc_id
  log_analytics_workspace_id  = module.monitoring.log_analytics_id
  enable_private_link         = var.enable_private_link
}

data "azurerm_client_config" "current" {}
