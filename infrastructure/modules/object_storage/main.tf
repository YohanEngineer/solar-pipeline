resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "bucket" {
  bucket = "${var.bucket_name_prefix}-${random_id.bucket_suffix.hex}"
  #acl    = "private"

  tags = {
    Environment = "poc"
  }
}