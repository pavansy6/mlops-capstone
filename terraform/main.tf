terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

resource "docker_image" "mlops_app_image" {
  name         = "pavansyadav/mlops-capstone:latest"
  keep_locally = false
}

resource "docker_container" "mlops_app_container" {
  image = docker_image.mlops_app_image.image_id
  name  = "mlops-capstone-container"
  ports {
    internal = 8000
    external = 8000
  }
}