from converter import Converter # TODO: Figure out library from PIP
import boto3

path_for_converted_images = "converted-videos/" # TODO: Move all configs to separate config file

def converter(file_name):
    c = Converter()

    info = c.probe(file_name)

    output_file = file_name.split('.')[0] + ".avi"

    conv = c.convert(file_name, output_file, {
        'format': 'mkv',
        'audio': {
            'codec': 'mp3',
            'samplerate': 11025,
            'channels': 2
        },
        'video': {
            'codec': 'theora',
            'width': 720,
            'height': 400,
            'fps': 15
        }})

    for timecode in conv:
        print("Converting (%f) ...\r" % timecode)

    return output_file

def main():
    sqs = boto3.client('sqs')
    queue_url = sqs.get_queue_url(QueueName = 'VideoProcessingQueue')['QueueUrl']
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    for message in response['Messages']: # TODO: Remove loop since only 1 message available
        body = eval(message['Body'])
        bucket = body['Records'][0]['s3']['bucket']['name']
        s3_object = body['Records'][0]['s3']['object']['key']
        file_name = s3_object.split('/')[-1]
        s3_download(bucket, s3_object, file_name)
        output_file = converter(file_name)
        s3_upload(bucket, output_file)

def s3_download(bucket, s3_object, file_name):
    s3 = boto3.client('s3')
    s3.download_file(bucket, s3_object, file_name)

def s3_upload(bucket, file_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket, f"{path_for_converted_images}{file_name}")


if __name__ = "__main__":
    main()