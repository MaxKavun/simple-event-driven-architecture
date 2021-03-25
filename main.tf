terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.26"
    }
  }
  backend "s3" {
    bucket = "my-test-bucket-maxkavun-dev	"
    key    = "terraform/dev-env"
    region = "eu-north-1"
  }
}

provider "aws" {
  region = "eu-north-1"
}

resource "aws_iam_role" "role_for_lambda" {
  name               = var.lambda_role_name
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
        "Action": "sts:AssumeRole",
        "Principal": {
            "Service": "lambda.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
        }
    ]
}
EOF
}

resource "aws_iam_policy" "lambda_necessary_policies" {
  name   = var.lambda_role_policy_name
  policy = file("${path.module}/lambda_policies.txt")
}

resource "aws_iam_role_policy_attachment" "lambda-attach" {
  role       = aws_iam_role.role_for_lambda.name
  policy_arn = aws_iam_policy.lambda_necessary_policies.arn
}

data "archive_file" "lambda_func" {
  type        = "zip"
  source_file = "${path.module}/scripts/lambda_function.py"
  output_path = "${path.module}/scripts/lambda.zip"
}

resource "aws_sqs_queue" "dead_letter_queue_for_converter" {
  name                       = var.dead_letter_queue_name
  visibility_timeout_seconds = var.sqs_dead_letter_queue_visibility_timeout
  message_retention_seconds  = var.message_retention_seconds
}

resource "aws_sqs_queue" "image_to_convert_queue" {
  name                       = var.sqs_queue_name
  visibility_timeout_seconds = var.sqs_timeout_visibility
  message_retention_seconds  = var.sqs_retention_period
  policy                     = file("sqs_policy.json")
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dead_letter_queue_for_converter.arn
    maxReceiveCount     = var.sqs_dead_letters_count
  })
}

resource "aws_lambda_function" "converter_func" {
  runtime       = "python3.8"
  filename      = "${path.module}/scripts/lambda.zip"
  function_name = var.lambda_name
  role          = aws_iam_role.role_for_lambda.arn
  handler       = var.lambda_handler

  environment {
    variables = {
      email_sender = var.email_sender
    }
  }
}

resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn = aws_sqs_queue.image_to_convert_queue.arn
  function_name    = aws_lambda_function.converter_func.arn
}

resource "aws_s3_bucket" "bucket" {
  bucket        = var.s3_name
  acl           = "private"
  force_destroy = true
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.bucket.id

  queue {
    queue_arn     = aws_sqs_queue.image_to_convert_queue.arn
    events        = var.s3_notification_events
    filter_prefix = var.s3_path_for_images_input
  }
}