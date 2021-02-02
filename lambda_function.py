import boto3
import json

path_for_converted_images = "text-documents/" # TODO: Move all configs to separate config file

# lambda tmp has 512 MB space

def lambda_handler(event, context):
    body = eval(event['Records'][0]['body'])
    bucket = body['Records'][0]['s3']['bucket']['name']
    s3_object = body['Records'][0]['s3']['object']['key']
    file_name = "/tmp/" + s3_object.split('/')[-1]
    s3_download(bucket, s3_object, file_name)
    output_file = pic_to_text(file_name)
    s3_upload(bucket, output_file)
    s3_remove_object(bucket, s3_object)

def s3_download(bucket, s3_object, file_name):
    s3 = boto3.client('s3')
    s3.download_file(bucket, s3_object, file_name)

def s3_upload(bucket, file_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket, f"{path_for_converted_images}{file_name.split('/')[-1]}")

def s3_remove_object(bucket, object_path):
    s3 = boto3.client('s3')
    response = s3.delete_object(
        Bucket=bucket,
        Key=object_path
    )

def pic_to_text(file_name):
    client = boto3.client('textract')
    picture = open(file_name, "rb")
    picture_bytes = bytearray(picture.read())
    picture.close()
    response = client.detect_document_text(
        Document={
            'Bytes': picture_bytes
        }
    )
    path_to_txt_file = file_name.split('.')[0] + ".txt"
    converted_txt = open(path_to_txt_file, "w")
    for line in response['Blocks']:
        if line['BlockType'] == "LINE":
            converted_txt.write(line['Text'] + "\n")
    converted_txt.close()
    return path_to_txt_file

if __name__ == "__main__":
    lambda_handler(event={'Records': [{'messageId': '5667d277-e288-4cd4-b8cb-3ac7e79cf55e', 'receiptHandle': 'AQEBMrLQ9YsHH4qzEwoQwxmZsxsSnCp9vA1M1sElOQ6qo9OZfONPLcVq6Y5JfaZkvZD4hoXMYL69DQSMa3c8PxOY+P7N2tZm9gYTqUhabnmlDHPBZ0civ+HUe1aQm+kEHZWB+manTBOzg8GEnisjnYjh71Cc0FJxnYGUOB0GAjPK3mbK+ON2Dk/RN+LRKjQAllxRsfI05dHi0gMiNw9bbMUa8JXGypr08fR904KRL5Rp93g4kpDsxbhyzJJowL8hGj+OJRRfx4iVzxKbS6L1XjMwd5IJbzU3OdBTeHl0/SabXjMPfnX0SKAx0HXvW7jSlTBCEv+Mx5wbUee+Xxp5a6ERVg9A5nqpITX2j5x58+exajXcq57b22CSL8Xw1yAyUdSX', 'body': '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"eu-west-1","eventTime":"2021-02-01T09:12:06.914Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"A37XF8K5LN9W2M"},"requestParameters":{"sourceIPAddress":"217.21.56.15"},"responseElements":{"x-amz-request-id":"E31492BD4045758B","x-amz-id-2":"rXvZVPvPuj32tQeSlY2YZylJtltUHPlWGtlTyQXao7zZ6gGX7t8HwAZNdZo3fZ/lx31O8t2gRg55aOf+lkvONuzDyEBK4/sf"},"s3":{"s3SchemaVersion":"1.0","configurationId":"add_message_to_queue","bucket":{"name":"max2021videocoder","ownerIdentity":{"principalId":"A37XF8K5LN9W2M"},"arn":"arn:aws:s3:::max2021videocoder"},"object":{"key":"images-to-extract/approve.JPG","size":12626,"eTag":"c2d2e8c59fcb289ee2783016a92acb11","sequencer":"006017C5E97DC87146"}}}]}', 'attributes': {'ApproximateReceiveCount': '1', 'SentTimestamp': '1612170730640', 'SenderId': 'AIDAJQOC3SADRY5PEMBNW', 'ApproximateFirstReceiveTimestamp': '1612170730645'}, 'messageAttributes': {}, 'md5OfBody': 'f4d9bcd3bc81974636c51b6896ce90a4', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:eu-west-1:673907469822:QueueOfVideos', 'awsRegion': 'eu-west-1'}]}, context=True)