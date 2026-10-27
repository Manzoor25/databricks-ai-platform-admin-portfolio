variable "subscription_id" {
  type        = string
  description = "Azure subscription that owns this lab."
}

variable "location" {
  type        = string
  description = "Azure region. Must support Model Serving, Foundation Model APIs, AI Search, and serverless. See ADR-0001."
  default     = "eastus"
}

variable "project" {
  type    = string
  default = "dbx-ai-admin"
}

variable "environment" {
  type    = string
  default = "lab"
}

variable "owner" {
  type    = string
  default = "mamoh"
}

variable "cost_center" {
  type    = string
  default = "personal-portfolio"
}

variable "monthly_budget_usd" {
  type        = number
  description = "Azure budget on the resource group. Alerts at 50/80/100 percent."
  default     = 150
}

variable "alert_email" {
  type        = string
  description = "Email for budget and action-group alerts."
  default     = "mamoh@microsoft.com"
}

variable "enable_private_link" {
  type        = bool
  description = "Front-end / storage private endpoints. Off by default (cost). See ADR-0003."
  default     = false
}

variable "enable_gpu" {
  type        = bool
  description = "Create classic GPU instance pool and allow GPU cluster policy to be assigned. No GPU VMs are started by apply."
  default     = false
}

variable "databricks_account_id" {
  type        = string
  description = "Azure Databricks account ID (account console). Required for metastore and account-level groups."
  default     = ""
}

variable "databricks_account_host" {
  type    = string
  default = "https://accounts.azuredatabricks.net"
}

variable "vnet_address_space" {
  type    = string
  default = "10.40.0.0/16"
}

variable "public_subnet_cidr" {
  type    = string
  default = "10.40.1.0/24"
}

variable "private_subnet_cidr" {
  type    = string
  default = "10.40.2.0/24"
}

variable "tags" {
  type = map(string)
  default = {
    data-classification = "public-and-synthetic"
    data-source         = "fdic-public-api"
  }
}
