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
