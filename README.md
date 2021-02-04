# Simple event driver architecture
An event-driven architecture uses events to trigger and communicate between decoupled services and is common in modern applications built with microservices.

Event-driven architectures have three key components: event producers, event routers, and event consumers. A producer publishes an event to the router, which filters and pushes the events to consumers. Producer services and consumer services are decoupled, which allows them to be scaled, updated, and deployed independently.

## About app

Based on S3 + SQS + Lambda + SNS + Textract. Fully serveless

Function is able to extract all images which can be recognized by AWS Textract service.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.14.5 |
| aws | >= 3.26 |

## Usage (default folder for upload images is images/)

```
terraform init
terraform apply -var-file="default.tfvars"
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| lambda\_role\_name | Lambda role name | `string` | `role_for_lambda` | yes |
| lambda_role_policy_name | Lambda role name | `string` | `lambda_policies` | yes |
| dead_letter_queue_name | Lambda role name | `string` | `dead-letter-queue-for-converter` | yes |
| sqs_queue_name | Lambda role name | `string` | `images-to-convert` | yes |
| lambda_name | Lambda role name | `string` | `pic_to_text_converter` | yes |
| s3_name | Lambda role name | `string` | `images-hosting-for-test-2021` | yes |
| sqs_timeout_visibility | Lambda role name | `number` | `240` | yes |
| sqs_retention_period | Lambda role name | `number` | `345600` | yes |
| sqs_dead_letters_count | Lambda role name | `number` | `4` | yes |
| lambda_handler | Lambda role name | `string` | `lambda_function.lambda_handler` | yes |
| s3_path_for_images_input | Lambda role name | `string` | `images/` | yes |
| s3_path_for_images_output | Lambda role name | `string` | `text-documents/` | yes |
| s3_notification_events | Lambda role name | `list(string)` | `["s3:ObjectCreated:*"]` | yes |
| sqs_dead_letter_queue_visibility_timeout | Lambda role name | `number` | `60` | yes |
| message_retention_seconds | Lambda role name | `number` | `1209600` | yes |

## Outputs

## TODO

- S3 presigned URL
- email notifications
> upload image > s3 event triggers Lambda > generate text, upload to S3 + generate S3 pre-sign URL for public usage + send it to email

