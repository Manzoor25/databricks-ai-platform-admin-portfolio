.PHONY: up down plan validate fmt lint test verify bootstrap idle

TF_DIR := infra

up:
	powershell -ExecutionPolicy Bypass -File scripts/up.ps1

down:
	powershell -ExecutionPolicy Bypass -File scripts/teardown.ps1

idle:
	powershell -ExecutionPolicy Bypass -File scripts/idle.ps1

plan:
	cd $(TF_DIR) && terraform plan -var-file=terraform.tfvars

validate:
	cd $(TF_DIR) && terraform fmt -check -recursive && terraform validate

fmt:
	cd $(TF_DIR) && terraform fmt -recursive

lint:
	ruff check project-1-governed-lakehouse-platform project-2-genai-rag-ai-gateway project-3-genie-mlops-model-governance scripts
	black --check project-1-governed-lakehouse-platform project-2-genai-rag-ai-gateway project-3-genie-mlops-model-governance scripts

test:
	pytest -q

verify:
	powershell -ExecutionPolicy Bypass -File scripts/verify.ps1

bootstrap:
	powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1
