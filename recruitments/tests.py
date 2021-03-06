import json, jwt

from django.test           import TestCase, Client
from django.conf           import settings

from recruitments.models   import *
from resumes.models        import Resume
from users.models          import *
from companies.models      import *

class RecruitmentsListTest(TestCase):
    def setUp(self):
        OccupationCategory.objects.create(
            id                  = 1,
            name                = '개발자'
        )
        OccupationSubcategory.objects.create(
            id                  = 1,
            name                = '백엔드',
            occupation_category = OccupationCategory(id=1)
        )
        Country.objects.create(
            id                  = 1,
            name                = '한국'
        )
        Province.objects.create(
            id                  = 1,
            name                = '서울',
            country             = Country(id=1)
        )
        DetailArea.objects.create(
            id                  = 1,
            name                = '강남구',
            province            = Province(id=1)
        )
        Company.objects.create(
            id                  = 1,
            name                = '회사',
            description         = '설명',
            detail_area         = DetailArea(id=1)
        )
        CompanyImage.objects.create(
            id                  = 1,
            image_url           = 'test.jpg',
            company             = Company(id=1)
        )
        Tag.objects.create(
            id                  = 1,
            name                = '워라밸'
        )
        TagCompany.objects.create(
            id                  = 1,
            company             = Company(id=1),
            tag                 = Tag(id=1)
        )
        Recruitment.objects.create(
            id                     = 1,
            name                   = '제목',
            description            = '설명',
            compensation           = 1000,
            deadline               = '2022-03-01',
            address                = '테헤란로',
            company                = Company(id=1),
            occupation_subcategory = OccupationSubcategory(id=1)
        )
    def tearDown(self):
        OccupationCategory.objects.all().delete()
        OccupationSubcategory.objects.all().delete()
        Country.objects.all().delete()
        Province.objects.all().delete()
        DetailArea.objects.all().delete()
        Company.objects.all().delete()
        Tag.objects.all().delete()
        TagCompany.objects.all().delete()
        Recruitment.objects.all().delete()
        
    def test_get_recruitment_list_success(self):
        client = Client()
        
        response =  client.get('/recruitments?category=1&subcategory=1&country=한국&province=서울&detail=강남구&tag=1')
        
        self.assertEqual(response.json(), 
            {
                "Recruitment": [
                    {
                        "company_name" : "회사",
                        "compensation" :1000,
                        "country": "한국",
                        "id": 1,
                        "logo_image": {
                            "image": "test.jpg"
                        },
                        "name": "제목",
                        "province": "서울"
                    }
                ],
                "message": "SUCCESS"
            }
        )

    def test_get_recruitment_detail_view_success(self):
        client = Client()

        response =  client.get('/recruitments/1')
        
        self.assertEqual(response.json(), 
            {
                "message": "SUCCESS",
                "result": {
                    "address": "테헤란로",
                    'company_id': 1,
                    "company_name": "회사",
                    "compensation": 1000,
                    "country": "한국",
                    "deadline": "2022-03-01",
                    "description": '설명',
                    "id": 1,
                    'image': [{'image': 'test.jpg'}],
                    "name": "제목",
                    'occupation_subcategory_id': 1,
                    "province": "서울",
                    'tags': [{'tag': '워라밸'}]
                }
            }
        )

class ApplicationTest(TestCase):
    def setUp(self):
        OccupationCategory.objects.create(
            id                  = 1,
            name                = '개발자'
        )
        OccupationSubcategory.objects.create(
            id                  = 1,
            name                = '백엔드',
            occupation_category = OccupationCategory(id=1)
        )
        Country.objects.create(
            id                  = 1,
            name                = '한국'
        )
        Province.objects.create(
            id                  = 1,
            name                = '서울',
            country             = Country(id=1)
        )
        DetailArea.objects.create(
            id                  = 1,
            name                = '강남구',
            province            = Province(id=1)
        )
        Company.objects.create(
            id                  = 1,
            name                = '회사',
            description         = '설명',
            detail_area         = DetailArea(id=1)
        )
        CompanyImage.objects.create(
            id                  = 1,
            image_url           = 'test.jpg',
            company             = Company(id=1)
        )
        Tag.objects.create(
            id                  = 1,
            name                = '워라밸'
        )
        TagCompany.objects.create(
            id                  = 1,
            company             = Company(id=1),
            tag                 = Tag(id=1)
        )
        Recruitment.objects.create(
            id                     = 1,
            name                   = '제목',
            description            = '설명',
            compensation           = 1000,
            deadline               = '2022-03-01',
            address                = '테헤란로',
            company                = Company(id=1),
            occupation_subcategory = OccupationSubcategory(id=1)
        )
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
        User.objects.create(
            id = 1,
            social_login = SocialLogin.objects.get(id=1),
            occupation_subcategory = OccupationSubcategory.objects.get(id=1)
        )
        ApplicationStatus.objects.create(
            id = 1,
            name = '성공'
        )
        Application.objects.create(
            id = 1,
            user_id = 1,
            recruitment_id = 1,
            application_status_id = 1
        )
        Resume.objects.create(
            id = 1,
            document = 'hola',
            name = 'hola',
            user_id = 1
        )
        ResumeApplication.objects.create(
            id = 1,
            application_id = 1,
            resume_id = 1
        )
    def tearDown(self):
        OccupationCategory.objects.all().delete()
        OccupationSubcategory.objects.all().delete()
        Country.objects.all().delete()
        Province.objects.all().delete()
        DetailArea.objects.all().delete()
        Company.objects.all().delete()
        Tag.objects.all().delete()
        TagCompany.objects.all().delete()
        Recruitment.objects.all().delete()
        SocialCompany.objects.all().delete()
        SocialLogin.objects.all().delete()
        User.objects.all().delete()
        ApplicationStatus.objects.all().delete()
        Application.objects.all().delete()
        Resume.objects.all().delete()
        ResumeApplication.objects.all().delete()
    
    def test_post_application_success(self):
        client = Client()
                
        application_data = {
            "resume_id" : [1]
        }
        access_token = jwt.encode({'user_id': 1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization" : access_token}
        response     =  client.post('/recruitments/applications/1', json.dumps(application_data), content_type='application/json', **headers)
        
        
        self.assertEqual(response.status_code, 201)

    
