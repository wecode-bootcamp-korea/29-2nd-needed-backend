import boto3, uuid
from needed.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS

class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id     = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        )
        self.bucket_name = AWS_STORAGE_BUCKET_NAME

    def upload(self, file):
        resume_uuid = 'resume/' + str(uuid.uuid4())
        self.s3.upload_fileobj(
                file,
                self.bucket_name,
                resume_uuid,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            ) 
        return AWS + resume_uuid
