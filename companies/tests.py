import json

from django.test    import TestCase, Client

from recruitments.models   import *
from companies.models      import *

class CompanyViewTest(TestCase):
    def setUp(self):
        OccupationCategory.objects.create(
            name                = '개발자'
        )
        OccupationSubcategory.objects.create(
            name                = '백엔드',
            occupation_category_id = 1
        )
        Country.objects.create(
            name                = '한국'
        )
        Province.objects.create(
            name                = '서울',
            country             = Country(id=1)
        )
        DetailArea.objects.create(
            name                = '강남구',
            province            = Province(id=1)
        )
        Company.objects.create(
            name                = '회사',
            description         = '설명',
            detail_area         = DetailArea(id=1)
        )
        CompanyImage.objects.create(
            image_url           = 'test.jpg',
            company             = Company(id=1)
        )
        Tag.objects.create(
            name                = '워라밸'
        )
        TagCompany.objects.create(
            company             = Company(id=1),
            tag                 = Tag(id=1)
        )
        Recruitment.objects.create(
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
        
    def test_get_company_detail_view_success(self):
        client = Client()
        
        response =  client.get('/companies/1')
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),     {
                    "message": "SUCCESS",
                    "result": {
                        "description": "설명",
                        "id": 1,
                        "images": [
                            {
                                "image": "test.jpg"
                            },
                        ],
                        "name": "회사",
                        "recruitments": [
                            {
                                "compensation": 1000,
                                "deadline": "2022-03-01",
                                "name": "제목"
                            },
                        ],
                        "tags": [
                            {
                                "name": "워라밸"
                            },
                        ]
                    }
                }
            )
