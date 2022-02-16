import json, jwt
from unittest.mock import patch, MagicMock

from django.test                    import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf                    import settings
from unittest.mock                  import MagicMock, patch

from recruitments.models import OccupationCategory, OccupationSubcategory

from .models import *
from users.models import *

class ResumeTest(TestCase):
    def setUp(self):
        SocialCompany.objects.create(
            id = 1,
            name = 'kakao'
        )

        SocialLogin.objects.create(
            id = 1,
            name = 'shawn',
            identification_number = 1234,
            social_company = SocialCompany.objects.get(id=1)
        )

        OccupationCategory.objects.create(
            id = 1,
            name = 'category'
        )

        OccupationSubcategory.objects.create(
            id = 1,
            name = 'sub_category',
            occupation_category = OccupationCategory.objects.get(id=1)
        )

        User.objects.create(
            id = 1,
            social_login = SocialLogin.objects.get(id=1),
            occupation_subcategory = OccupationSubcategory.objects.get(id=1)
        )

        Resume.objects.create(
            id = 1,
            document = 'test',
            user     = SocialLogin.objects.get(id=1)
        )
        self.token = jwt.encode({'user_id' : 1}, settings.SECRET_KEY, settings.ALGORITHM)

    def tearDown(self):
        SocialCompany.objects.all().delete()
        SocialLogin.objects.all().delete()
        OccupationCategory.objects.all().delete()
        User.objects.all().delete()
        Resume.objects.all().delete()
        
    

    @patch('resumes.views.boto3.client')
    def test_resume_s3_upload_success(self, mocked_client):
        client = Client()

        document = SimpleUploadedFile(
                'test.png',
                b'file_content',
                content_type='image/png'
        )
        

        class MockedResponse:
            def upload(self,file):
                return 'https://29needed.s3.ap-northeast-2.amazonaws.com/resumes'

        mocked_client.upload = MagicMock(return_value=MockedResponse())
        header = {'HTTP_Authorization' : self.token, 'ContentType' : 'multipart/form-data'}
        response = client.post('/resumes', document, **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'message': 'SUCCESS'})
