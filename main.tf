terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.26"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_iam_role" "role_for_lambda" {
  name               = "role_for_lambda"
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
  name   = "lambda_policies"
  policy = file("${path.module}/lambda_policies.txt")
}

resource "aws_iam_role_policy_attachment" "lambda-attach" {
  role       = aws_iam_role.role_for_lambda.name
  policy_arn = aws_iam_policy.lambda_necessary_policies.arn
}

data "archive_file" "lambda_func" {
  type        = "zip"
  source_file  = "${path.module}/lambda_function.py"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "converter_func" {
  runtime       = "python3.8"
  filename      = "${path.module}/lambda.zip"
  function_name = "pic_to_text_converter"
  role          = aws_iam_role.role_for_lambda.arn
  handler       = "lambda_function.lambda_handler"
}