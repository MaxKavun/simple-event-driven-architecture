# Simple event driver architecture
An event-driven architecture uses events to trigger and communicate between decoupled services and is common in modern applications built with microservices.

Event-driven architectures have three key components: event producers, event routers, and event consumers. A producer publishes an event to the router, which filters and pushes the events to consumers. Producer services and consumer services are decoupled, which allows them to be scaled, updated, and deployed independently.

### About app

Based on S3 + SQS + Lambda + SNS + Textract. Fully serveless

Function is able to extract all images which can be recognized by AWS Textract service.

### Usage (default folder for upload imags is images/)

'''
terraform init
terraform apply -var-file="default.tfvars
'''

### TODO

- S3 presigned URL
- email notifications
> upload image > s3 event triggers Lambda > generate text, upload to S3 + generate S3 pre-sign URL for public usage + send it to email