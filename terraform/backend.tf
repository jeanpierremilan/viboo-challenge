

terraform {
  required_version = ">= 1.3.1, < 2.0.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.2.0"
    }
  }
  backend "gcs" {
    impersonate_service_account = "terraform-dev@{var.project_id}.iam.gserviceaccount.com"
    bucket                      = "viboo-challenge-tf-state"
    prefix                      = "backend"
  }
}