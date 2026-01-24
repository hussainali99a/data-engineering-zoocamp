terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  # Configuration options
  credentials = "/workspaces/data-engineering-zoocamp/terraform-demo/keys/my-creds.json"
  project = "single-loop-463705-t0"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "data-eng-zoocamp-demo-bucket-terra01"
  location      = "US"
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}


resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id  = "demo_dataset"
}