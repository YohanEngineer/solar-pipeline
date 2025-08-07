resource "aws_kinesis_stream" "solar_stream" {
  name             = "terraform-kinesis-solar"
  shard_count      = 1
  retention_period = var.retention_period

  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]

  tags = {
    Environment = "poc"
  }
}
