provider "aws" {
  region = "eu-west-2"  # London region, change if needed
}

resource "aws_s3_bucket" "agentic_storage" {
  bucket = "agentic-platform-${random_id.bucket_id.hex}"
  force_destroy = true
}

resource "random_id" "bucket_id" {
  byte_length = 4
}
