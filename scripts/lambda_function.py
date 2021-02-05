import boto3
import json
import os

path_for_converted_images = "text-documents/" # TODO: Move all configs to separate config file

# lambda tmp has 512 MB space

def lambda_handler(event, context):
    body = eval(event['Records'][0]['body'])
    if ('Records' not in body):
        return True
    bucket = body['Records'][0]['s3']['bucket']['name']
    s3_object = body['Records'][0]['s3']['object']['key']
    file_name = "/tmp/" + s3_object.split('/')[-1]
    s3_download(bucket, s3_object, file_name)
    output_file = pic_to_text(file_name)
    path_for_object = s3_upload(bucket, output_file)
    presigned_url = s3_generate_presigned_url(bucket, path_for_object)
    ses_send_email(presigned_url)
    s3_remove_object(bucket, s3_object)

def s3_download(bucket, s3_object, file_name):
    s3 = boto3.client('s3')
    s3.download_file(bucket, s3_object, file_name)

def s3_upload(bucket, file_name):
    s3 = boto3.client('s3')
    path_for_object = f"{path_for_converted_images}{file_name.split('/')[-1]}"
    s3.upload_file(file_name, bucket, path_for_object)
    return path_for_object

def s3_remove_object(bucket, object_path):
    s3 = boto3.client('s3')
    response = s3.delete_object(
        Bucket=bucket,
        Key=object_path
    )

def s3_generate_presigned_url(bucket, object_path, expiration=3600):
    s3_client = boto3.client('s3')
    response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket,
                                                            'Key': object_path},
                                                    ExpiresIn=expiration)
    return response

def ses_send_email(presigned_url):
    ses_client = boto3.client('ses')
    charset = "UTF-8"
    sender = os.environ['email_sender']
    recipient = ["maksim_kavun@epam.com"] # TODO: recepient should come from object tag
    subject = "Your link to the converted image"

    body_html = f"""<html>
                <head></head>
                <body>
                <h2>Your link to the converted image</h2>
                <p>{presigned_url}</p>
                </body>
                </html>
                """ 
    response = ses_client.send_email(
        Destination={
            "ToAddresses": recipient,
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": charset,
                    "Data": body_html,
                }
            },
            "Subject": {
                "Charset": charset,
                "Data": subject,
            },
        },
        Source=sender,
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