module "object_storage" {
  source             = "../modules/object_storage"
  bucket_name_prefix = "solar-poc"
}

module "streaming_sink" {
  source = "../modules/streaming_sink"
}

module "streaming_consumer" {
  source             = "../modules/streaming_consumer"
  bucket_arn         = module.object_storage.bucket_arn
  kinesis_stream_arn = module.streaming_sink.kinesis_stream_arn
}
