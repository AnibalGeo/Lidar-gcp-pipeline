# 1. Definición del Proveedor de Google Cloud
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "geomatica-portfolio"
  region  = "europe-west1" # Cambia la región si prefieres usar una de EE.UU. como us-central1
}

# 2. Creación del Repositorio en Artifact Registry para Docker
resource "google_artifact_registry_repository" "lidar_repo" {
  location      = "europe-west1"
  repository_id = "lidar-tool-repo"
  description   = "Repositorio Docker para el procesamiento automatizado de LiDAR"
  format        = "DOCKER"

  docker_config {
    immutable_tags = false
  }
}

# 3. Asegurar la existencia del Bucket de almacenamiento (GCS)
resource "google_storage_bucket" "lidar_bucket" {
  name          = "lidar-pnoa-portfolio"
  location      = "EU" # O "US" si cambiaste la región arriba
  force_destroy = false

  uniform_bucket_level_access = true
}
