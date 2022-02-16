import boto3, uuid
from django.conf import settings

class S3Client:
    def __init__(self, access_key, secret_access_key, bucket_name):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id     = access_key,
            aws_secret_access_key = secret_access_key
        )
        self.bucket_name = bucket_name

    def upload(self, file, folder_name):   
        key = folder_name + str(uuid.uuid4())
        self.s3.upload_fileobj(
                file,
                self.bucket_name,
                key,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            ) 
        return settings.AWS + key
