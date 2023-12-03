
module "project-factory-viboo" {
  source  = "terraform-google-modules/project-factory/google"
  version = "~> 10.1"

  
  name                        = var.project-id
  project_id                  = var.project-id
  folder_id                   = var.folder-id
  org_id                      = var.org-id


  billing_account             = var.billing-account
  auto_create_network         = false
  
  default_service_account     = "keep"  
  
}

module "bucket-viboo-challenge" {
  source  = "terraform-google-modules/cloud-storage/google//modules/simple_bucket"
  version = "~> 1.3"

  name       = "viboo-challenge"
  project_id = var.project-id
  location   = "europe-west6"
  iam_members = []

  versioning=false
}

resource "google_cloudbuild_trigger" "viboo-cicd" {
  location = var.region
  project  = var.project-id
  name     = "viboo-challenge"
  filename = "cloudbuild.yaml"
  service_account = "projects/${var.project-id}/serviceAccounts/project-service-account@${var.project-id}.iam.gserviceaccount.com"

  included_files = ["/*" ]

  github {
    owner  = "jeanpierremilan"
    name   = "viboo-challenge"
    push {
      branch = "^main$"
    }
  }

  include_build_logs = "INCLUDE_BUILD_LOGS_WITH_STATUS"
}

resource "google_artifact_registry_repository" "docker-viboo-challenge" {
  provider = google
  project = var.project-id
  location = "europe-west6"
  repository_id = "viboo"
  description = "viboo backend"
  format = "DOCKER"
  cleanup_policy_dry_run =true
}