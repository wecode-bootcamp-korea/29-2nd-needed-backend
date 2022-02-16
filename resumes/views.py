import boto3

from django.views  import View
from django.http   import JsonResponse
from django.conf   import settings
from django.db     import transaction

from core.utils    import authorization
from core.storages import S3Client
from .models       import *
class ResumeView(View):
    @authorization
    def post(self, request):
        try:
            with transaction.atomic():
                resume_file = request.FILES.get('document', None)
                s3_client   = S3Client(settings.AWS_ACCESS_KEY_ID, 
                                        settings.AWS_SECRET_ACCESS_KEY, 
                                        settings.AWS_STORAGE_BUCKET_NAME)

                resume = Resume(
                    document = s3_client.upload(resume_file, 'resume/'),
                    user     = request.user             
                )

                resume.save()

                return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except KeyError as e:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
