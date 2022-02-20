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
