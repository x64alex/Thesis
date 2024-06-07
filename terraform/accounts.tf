resource "google_service_account" "circleci_service_account" {
  account_id   = "circleci-service-account"
  display_name = "CircleCI Service Account"
}

resource "google_project_iam_binding" "artifact_registry_writer" {
  project = "investmentbot-425621"
  role    = "roles/artifactregistry.writer"

  members = [
    "serviceAccount:${google_service_account.circleci_service_account.email}"
  ]
}

resource "google_project_iam_binding" "storage_admin" {
  project = "investmentbot-425621"
  role    = "roles/storage.admin"

  members = [
    "serviceAccount:${google_service_account.circleci_service_account.email}"
  ]
}

resource "google_service_account_key" "circleci_service_account_key" {
  service_account_id = google_service_account.circleci_service_account.name
  keepers = {
    last_updated = filemd5("${path.module}/main.tf")
  }
  private_key_type = "TYPE_GOOGLE_CREDENTIALS_FILE"
}

output "circleci_service_account_key" {
  value     = google_service_account_key.circleci_service_account_key.private_key
  sensitive = true
}
