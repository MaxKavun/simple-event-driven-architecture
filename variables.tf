variable "lambda_role_name" {
  type = string
}
variable "lambda_role_policy_name" {
  type = string
}
variable "dead_letter_queue_name" {
  type = string
}
variable "sqs_queue_name" {
  type = string
}
variable "lambda_name" {
  type = string
}
variable "s3_name" {
  type = string
}
variable "sqs_timeout_visibility" {
  type = number
}
variable "sqs_retention_period" {
  type = number
}
variable "sqs_dead_letters_count" {
  type = number
}
variable "lambda_handler" {
  type = string
}
variable "s3_path_for_images_input" {
  type = string
}
variable "s3_path_for_images_output" { # TODO: Add ability to redefine output folder (hardcoded)
  type = string
}
variable "s3_notification_events" {
  type = list(string)
}
variable "sqs_dead_letter_queue_visibility_timeout" {
  type = number
}
variable "message_retention_seconds" {
  type = number
}
variable "email_sender" {
  type = string
}