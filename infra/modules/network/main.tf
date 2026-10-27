variable "name_prefix" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "tags" { type = map(string) }
variable "vnet_address_space" { type = string }
variable "public_subnet_cidr" { type = string }
variable "private_subnet_cidr" { type = string }

resource "azurerm_virtual_network" "this" {
  name                = "vnet-${var.name_prefix}"
  location            = var.location
  resource_group_name = var.resource_group_name
  address_space       = [var.vnet_address_space]
  tags                = var.tags
}

resource "azurerm_network_security_group" "public" {
  name                = "nsg-${var.name_prefix}-pub"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_network_security_group" "private" {
  name                = "nsg-${var.name_prefix}-prv"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_subnet" "public" {
  name                 = "snet-${var.name_prefix}-pub"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = [var.public_subnet_cidr]

  delegation {
    name = "databricks-public"
    service_delegation {
      name = "Microsoft.Databricks/workspaces"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
        "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action",
        "Microsoft.Network/virtualNetworks/subnets/unprepareNetworkPolicies/action",
      ]
    }
  }
}

resource "azurerm_subnet" "private" {
  name                 = "snet-${var.name_prefix}-prv"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = [var.private_subnet_cidr]

  delegation {
    name = "databricks-private"
    service_delegation {
      name = "Microsoft.Databricks/workspaces"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
        "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action",
        "Microsoft.Network/virtualNetworks/subnets/unprepareNetworkPolicies/action",
      ]
    }
  }
}

# Small subnet for optional private endpoints. Not delegated to Databricks.
resource "azurerm_subnet" "pe" {
  name                 = "snet-${var.name_prefix}-pe"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = [cidrsubnet(var.vnet_address_space, 8, 3)]
}

resource "azurerm_subnet_network_security_group_association" "public" {
  subnet_id                 = azurerm_subnet.public.id
  network_security_group_id = azurerm_network_security_group.public.id
}

resource "azurerm_subnet_network_security_group_association" "private" {
  subnet_id                 = azurerm_subnet.private.id
  network_security_group_id = azurerm_network_security_group.private.id
}

output "vnet_id" { value = azurerm_virtual_network.this.id }
output "public_subnet_name" { value = azurerm_subnet.public.name }
output "private_subnet_name" { value = azurerm_subnet.private.name }
output "public_nsg_assoc_id" { value = azurerm_subnet_network_security_group_association.public.id }
output "private_nsg_assoc_id" { value = azurerm_subnet_network_security_group_association.private.id }
output "pe_subnet_id" { value = azurerm_subnet.pe.id }
