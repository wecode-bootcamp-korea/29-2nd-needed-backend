import jwt
import json
import requests

from django.shortcuts import redirect
from django.http      import JsonResponse
from django.views     import View
from django.conf      import settings
from django.db.models import Case, When, Count, Avg

from core.utils          import KakaoAPI, authorization
from users.models        import SocialCompanyEnum, User, SocialCompany, SocialLogin
from recruitments.models import OccupationSubcategory

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
            
            if User.objects.filter(social_login = user.id).exists():
                return JsonResponse({'message': "SUCCESS",'result':kakao_user,'access_token' : jwt_token}, status=status_code)
            
            else:
                return JsonResponse({'message': "NEED_SIGNUP",'result':kakao_user,'access_token' : jwt_token}, status=status_code)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except SocialLogin.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=404)

class ProfileView(View):
    @authorization
    def post(self, request):
        try:
            user_data  = json.loads(request.body)
            occupation = user_data.get('occupation',None)
            
            data, created = User.objects.update_or_create(
                social_login  = request.user,
                defaults      = {
                    'phone_number'            : user_data.get('phone_number',None),
                    'address'                 : user_data.get('address',None),
                    'career'                  : user_data.get('career',None),
                    'salary'                  : user_data.get('salary',None),
                    'occupation_subcategory'  : OccupationSubcategory.objects.get(id = occupation) if occupation is not None else None 
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
        application_parameter = {
            'application_complete' : 1,
            'accepted_document'    : 2,
            'final_acceptance'     : 3,
            'fail_acceptance'      : 4
        }
        
        annotate_set = {key : Count(
                                Case(
                                    When(social_login__applications__application_status = value ,
                                        then = 'social_login__applications')
                                    )
                                )for key,value in application_parameter.items()}

        user = User.objects \
                    .select_related("social_login","occupation_subcategory__occupation_category") \
                    .annotate(**annotate_set) \
                    .get(social_login = request.user) 
        
        result = {
            'email'             : user.social_login.email,
            'profile_image'     : user.social_login.profile_image,
            'name'              : user.social_login.name,
            'job_category'      : user.occupation_subcategory.occupation_category.name if user.occupation_subcategory is not None else None,
            'job_subcategory'   : user.occupation_subcategory.name if user.occupation_subcategory is not None else None,
            'is_subscription'   : user.is_subscription,
            'subscription_date' : user.subscription_date,
            'phone_number'      : user.phone_number,
            'address'           : user.address,
            'career'            : user.career,
            'salary'            : user.salary,
            'application'       : [{
                'application_complete' : user.application_complete,
                'accepted_document'    : user.accepted_document,
                'final_acceptance'     : user.final_acceptance,
                'fail_acceptance'      : user.fail_acceptance
            }]
        }
        
        return JsonResponse({'message' : 'SUCCESS', 'result' : result}, status = 200)
    
class SalaryView(View):
    def get(self,request,occupation_id):
        try:
            occupation = OccupationSubcategory.objects.prefetch_related("users").filter(id = occupation_id)                    

            salary_avg_list = [occupation.filter(users__career = i+1) \
                                            .aggregate(Avg('users__salary')) \
                                            .get("users__salary__avg") for i in range(11)]
            
            result          = {f"salary_avg_career_{key}": value for key, value in enumerate(salary_avg_list)}
            
            return JsonResponse({'message' : 'SUCCESS', 'result' : result}, status = 200)
        
        except TypeError:
            return JsonResponse({'message' : 'DOES_NOT_EXIST_OCCUPATION'}, status = 404)
