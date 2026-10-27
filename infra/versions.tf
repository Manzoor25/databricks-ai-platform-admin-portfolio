terraform {
  required_version = ">= 1.9.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.40"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 3.4"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.85"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }

  # First apply uses local state (gitignored). After the storage account exists,
  # migrate with:
  #   terraform init -migrate-state -backend-config=backend.hcl
  # backend.hcl is written by scripts/bootstrap.ps1 and is gitignored.
  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy    = false
      recover_soft_deleted_key_vaults = true
    }
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
  subscription_id     = var.subscription_id
  storage_use_azuread = true
}

provider "azuread" {}

# Account-level provider is declared in account.tf and is only planned when
# databricks_account_id is set. Workspace provider is declared in workspace.tf
# after the workspace exists, so `terraform validate` does not need a live host.
