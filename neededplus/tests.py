import jwt

from datetime       import date
from django.test    import TestCase, Client
from django.conf    import settings

from users.models   import *

class NeededPlusTest(TestCase):
    def setUp(self):
        SocialCompany.objects.create(
            id   = 1,
            name = '카카오' 
        )
        SocialLogin.objects.create(
            id                    = 1,
            name                  = 'test',
            email                 = 'test123@gmail.com',
            identification_number = '132234245253',
            profile_image         = '123123123123.jpg',
            social_company        = SocialCompany.objects.get(id=1)
        )
        User.objects.create(
            id                    = 1,
            social_login          = SocialLogin.objects.get(id=1)
        )
        
    def tearDown(self):
        SocialCompany.objects.all().delete()
        SocialLogin.objects.all().delete()
        User.objects.all().delete()
        
    def test_needed_plus_subscribe_create_success(self):
        client = Client()
        
        access_token = jwt.encode({'user_id': 1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization" : access_token}
        response     =  client.patch('/neededplus', **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message" : "SUCCESS","result" : str(date.today())})
