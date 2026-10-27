locals {
  name_prefix = "${var.project}-${var.environment}"

  common_tags = merge(var.tags, {
    project     = var.project
    owner       = var.owner
    cost-center = var.cost_center
    environment = var.environment
    managed-by  = "terraform"
  })
}
