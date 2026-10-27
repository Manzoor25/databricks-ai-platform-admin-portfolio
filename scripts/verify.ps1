#Requires -Version 5.1
$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
Write-Host "== pytest =="
Push-Location (Join-Path $root "project-1-governed-lakehouse-platform"); python -m pytest -q; Pop-Location
Push-Location (Join-Path $root "project-2-genai-rag-ai-gateway"); python -m pytest -q; Pop-Location
Push-Location (Join-Path $root "project-3-genie-mlops-model-governance"); python -m pytest -q; Pop-Location
Write-Host "== terraform validate =="
Push-Location (Join-Path $root "infra"); terraform validate; Pop-Location
Write-Host "== workspace =="
az databricks workspace show --name dbw-dbx-ai-admin-lab --resource-group rg-dbx-ai-admin-lab --query "{name:name, sku:sku.name, url:workspaceUrl, state:provisioningState}" -o json
Write-Host "== metastore (expected to fail until an account admin assigns one) =="
$env:DATABRICKS_HOST = "https://adb-7405619764740124.4.azuredatabricks.net"
$env:DATABRICKS_AUTH_TYPE = "azure-cli"
databricks metastores current --output json
Write-Host "== gpu execution claim =="
Write-Host "No GPU workload has been executed. CPU evidence: evidence/cpu-train.json"
