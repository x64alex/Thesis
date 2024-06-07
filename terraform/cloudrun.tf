resource "google_cloud_run_service" "run_service" {
  name     = "backend"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/investmentbot-425621/docker-repo/investmentbot-425621/api:latest"
        
        ports {
          container_port = 5000
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_project_service.run_api]
}
