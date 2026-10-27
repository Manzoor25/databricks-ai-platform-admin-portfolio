#Requires -Version 5.1
<#
.SYNOPSIS
  Stop what can be stopped without deleting the workspace.
  As of 2026-10-27 there is no SQL warehouse, serving endpoint, or all-purpose cluster.
  This script checks, and exits without inventing work.
#>
$ErrorActionPreference = "Stop"
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
$env:DATABRICKS_HOST = "https://adb-7405619764740124.4.azuredatabricks.net"
$env:DATABRICKS_AUTH_TYPE = "azure-cli"
Write-Host "Warehouses:"
databricks warehouses list --output json
Write-Host "If a warehouse is running, stop it with: databricks warehouses stop <id>"
Write-Host "Workspace itself has no stop button. Teardown is scripts/teardown.ps1."
