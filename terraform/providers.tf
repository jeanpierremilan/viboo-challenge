provider "google" {
    credentials = var.credentials
}

provider "google-beta" {
    credentials = var.credentials
}