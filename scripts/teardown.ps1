#Requires -Version 5.1
<#
.SYNOPSIS
  Destroy billable resources in rg-dbx-ai-admin-lab. Keeps the code.
  Does not delete the resource group if Terraform state is missing; it tells you the az command.
#>
$ErrorActionPreference = "Stop"
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
Set-Location (Join-Path (Split-Path -Parent $PSScriptRoot) "infra")
if (Test-Path "terraform.tfstate") {
  terraform destroy "-var-file=terraform.tfvars" "-input=false" "-auto-approve" "-lock=false"
} else {
  Write-Host "No local state. Destroy the resource group directly:"
  Write-Host "az group delete --name rg-dbx-ai-admin-lab --yes --no-wait"
}
