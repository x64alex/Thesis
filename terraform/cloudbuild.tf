resource "google_cloudbuild_trigger" "test_trigger" {
  name     = "test-trigger"
  description = "Trigger for running tests"
  
  github {
    owner  = "x64alex"
    name   = "your-repository-name"
    push {
      branch = "main"
    }
  }

  filename = "cloudbuild.yaml"
}