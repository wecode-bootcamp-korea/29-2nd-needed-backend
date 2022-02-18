import jwt, json

from django.test    import TestCase, Client
from django.conf    import settings
from unittest       import mock
from unittest.mock  import patch

from users.models   import *

class KakaoSignInTest(TestCase):
    def setUp(self):
        SocialCompany.objects.create(
            id   = 1,
            name = '카카오' 
        )
    
    def tearDown(self):
        SocialLogin.objects.all().delete()
    
    @patch("core.utils.requests")
    def test_kakao_login_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            status_code = 200
            
            def json(self):
                return {
                    "id": 2145645622,
                    "connected_at": "2022-02-16T05:48:20Z",
                    "properties": {
                        "nickname": "김준영"
                    },
                    "kakao_account": {
                    "profile_nickname_needs_agreement": False,
                    "profile_image_needs_agreement": True,
                    "profile": {
                        "nickname": "김준영",
                        "thumbnail_image_url": "http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_110x110.jpg",
                        "profile_image_url": "http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_640x640.jpg",
                        "is_default_image": True
                    },
                    "has_email": True,
                    "email_needs_agreement": False,
                    "is_email_valid": True,
                    "is_email_verified": True,
                    "email": "junyoung6080@daum.net",
                    "has_gender": True,
                    }
                }

        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_access-token" : "1234"}
        response            = client.get("/users/signin/kakao/callback", **headers)

        self.assertEqual(response.status_code, 201)

    @patch("core.utils.requests")
    def test_kakao_signin_client_get_key_error(self, mocked_requests):
        client = Client()

        class MockedResponse:
            status_code = 200
            
            def json(self):

                return {
                    "id":114142,
                    "kakao_account": { 
                        "profile_needs_agreement": False,
                        "profile_nickname_needs_agreement": False,
                        "profile_image_needs_agreement": False,
                        "profile": {
                            "nickname": "김준영",
                            "thumbnail_image_url": "http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_110x110.jpg",
                            "profile_image_url": "http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_640x640.jpg",
                            "is_default_image":True
                            }
                        }
                    }

        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_access-token" : "a123423423412341234"} 
        response            = client.get("/users/signin/kakao/callback", **headers)
    
        self.assertEqual(response.json(), {'message' : "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)

class UserDataTest(TestCase):
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
        
    def tearDown(self):
        SocialCompany.objects.all().delete()
        SocialLogin.objects.all().delete()
        User.objects.all().delete()
        
    def test_user_mypage_data_create_success(self):
        client = Client()
        user_data = {
            'social_login'  : 1,
            'phone_number'  : '01018232345',
            'address'       : '테헤란로',
            'career'        : 1,
            'salary'        : 30000000,
            }
        
        access_token = jwt.encode({'user_id': 1}, settings.SECRET_KEY, settings.ALGORITHM)
        headers      = {"HTTP_Authorization" : access_token}
        response     =  client.post('/users/mypage', json.dumps(user_data), content_type='application/json', **headers)
        
        self.assertEqual(response.status_code, 201)
