output "kinesis_stream_arn" {
  description = "ARN of the kinesis stream"
  value       = aws_kinesis_stream.solar_stream.arn
}
