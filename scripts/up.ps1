#Requires -Version 5.1
$ErrorActionPreference = "Stop"
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
Set-Location (Join-Path (Split-Path -Parent $PSScriptRoot) "infra")
terraform init -input=false
terraform apply "-var-file=terraform.tfvars" "-input=false" "-lock=false"
