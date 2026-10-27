#Requires -Version 5.1
<#
.SYNOPSIS
  Phase 0/1 bootstrap: tool check, terraform init, and first apply.
.NOTES
  Does not print secrets. Interactive `az login` is required if the session expired.
#>
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location (Join-Path $root "infra")

$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
  [System.Environment]::GetEnvironmentVariable("Path", "User")

Write-Host "Terraform: $(terraform version | Select-Object -First 1)"
Write-Host "Azure account:"
az account show --query "{name:name,id:id,user:user.name}" -o json

if (-not (Test-Path ".terraform")) {
  terraform init -input=false
}

terraform fmt -recursive
terraform validate
terraform plan -var-file=terraform.tfvars -out=tfplan.lab -input=false
Write-Host "Plan written to infra/tfplan.lab (gitignored). Review, then apply with scripts/up.ps1."
