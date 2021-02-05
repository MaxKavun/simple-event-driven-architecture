lambda_role_name                         = "role_for_lambda"
lambda_role_policy_name                  = "lambda_policies"
dead_letter_queue_name                   = "dead-letter-queue-for-converter"
sqs_queue_name                           = "images-to-convert"
lambda_name                              = "pic_to_text_converter"
s3_name                                  = "images-hosting-for-test-2021"
sqs_timeout_visibility                   = 240
sqs_retention_period                     = 345600
sqs_dead_letters_count                   = 2
lambda_handler                           = "lambda_function.lambda_handler"
s3_path_for_images_input                 = "images/"
s3_path_for_images_output                = "text-documents/"
s3_notification_events                   = ["s3:ObjectCreated:*"]
sqs_dead_letter_queue_visibility_timeout = 60
message_retention_seconds                = 1209600
email_sender                             = "John Doe <johndoe@outlook.com>"