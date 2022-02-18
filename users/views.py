import jwt
import json
import requests

from django.shortcuts import redirect
from django.http      import JsonResponse
from django.views     import View
from django.conf      import settings

from core.utils       import KakaoAPI, authorization
from users.models     import SocialCompanyEnum, User, SocialCompany, SocialLogin

class KakaoSignInView(View):
    def get(self, request):
        return redirect(f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={settings.KAKAO_CLIENT_ID}&redirect_uri={settings.KAKAO_REDIRECT_URI}")

class KakaoCallBackView(View):
    def get(self, request):
        try:
            access_token   = request.headers.get('access-token')
            kakao_user     = KakaoAPI(access_token).get_user()

            kakao_id       = kakao_user['id']
            email          = kakao_user['kakao_account']['email']
            name           = kakao_user['kakao_account']['profile']['nickname']
            profile_image  = kakao_user['kakao_account']['profile']['thumbnail_image_url']

            user, created   = SocialLogin.objects.get_or_create(
                identification_number = kakao_id,
                social_company        = SocialCompany(SocialCompanyEnum.KAKAO.value),
                defaults              = {
                    'email'         : email,
                    'name'          : name,
                    'profile_image' : profile_image 
                }
            )

            status_code  = 201 if created else 200
            
            jwt_token = jwt.encode({'user_id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)
            
            return JsonResponse({'message': "SUCCESS",'result':kakao_user,'access_token' : jwt_token}, status=status_code)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except SocialLogin.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=404)

class ProfileView(View):
    @authorization
    def post(self, request):
        try:
            user_data = json.loads(request.body)
            
            data, created = User.objects.update_or_create(
                social_login  = request.user,
                defaults      = {
                    'phone_number': user_data.get('phone_number',None),
                    'address'     : user_data.get('address',None),
                    'career'      : user_data.get('career',None),
                    'salary'      : user_data.get('salary',None),
                    }
                )
            
            status_code = 201 if created else 204 
            
            return JsonResponse({'message' : 'SUCCESS'}, status=status_code)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)

    @authorization
    def get(self, request):
        user = User.objects.select_related("social_login").get(social_login = request.user) 

        result = {
            'email'         : user.social_login.email,
            'profile_image' : user.social_login.profile_image,
            'name'          : user.social_login.name,
            'phone_number'  : user.phone_number,
            'address'       : user.address,
            'career'        : user.career,
            'salary'        : user.salary,
        }
        
        return JsonResponse({'message' : 'SUCCESS', 'result' : result}, status = 200)
