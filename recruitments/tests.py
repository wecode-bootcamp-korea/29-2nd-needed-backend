import json
from unicodedata import name

from django.test    import TestCase, Client

from recruitments.models   import *
from companies.models      import *

class RecruitmentsListTest(TestCase):
    def setUp(self):
        OccupationCategory.objects.create(
            name                = '개발자'
        )
        OccupationSubcategory.objects.create(
            name                = '백엔드',
            occupation_category = OccupationCategory(id=1)
        )
        Country.objects.create(
            name                = '대한민국'
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
        Tag.objects.create(
            name                = '워라밸'
        )
        TagCompany.objects.create(
            company             = Company(id=1),
            tag                 = Tag(id=1)
        )
        Recruitment.objects.create(
            name                   = '제목',
            description             = '설명',
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
        
        response =  client.get('/recruitments?category=1&subcategory=1&country=대한민국&province=서울&detail=강남구&tag=1')
        
        self.assertEqual(response.json(), 
            {
                "Recruitment": [
                    {
                        "company_name": "회사",
                        "country": "대한민국",
                        "id": 1,
                        "name": "제목",
                        "province": "서울"
                    }
                ],
                "message": "SUCCESS"
            }
        )
