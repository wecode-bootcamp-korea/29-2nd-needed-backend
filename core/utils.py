import requests, re, jwt

from django.core.exceptions import ValidationError
from django.http            import JsonResponse

from users.models           import User

class KakaoAPI:
    def __init__(self, data):
        self.grant_type    = 'authorization_code'
        self.api_uri       = 'https://kapi.kakao.com/v2/'
        self.data          = data

    def get_token(self, grant_type, client_id,client_secret,redirect_uri):
        token_url = "https://kauth.kakao.com/oauth/token?grant_type={0}&client_id={1}&client_secret={2}&redirect_uri={3}&code={4}"\
            .format(
                    grant_type,
                    client_id,
                    client_secret,
                    redirect_uri,
                    self.data
                )
        headers = {
            'Content-Type' :'application/x-www-form-urlencoded'
            }
        
        response     = requests.post(token_url,headers=headers)
        access_token = response.json()['access_token']
        
        if response.status_code == 401:
            return JsonResponse({'MESSAGE': 'INVALID_CLIENT'}, status=400)
        
        return access_token

    def get_user(self):
        headers  = {"Authorization" : f"Bearer {self.data}"}
        response = requests.get(f"{self.api_uri}/user/me", headers=headers, timeout = 5)
        
        if not response.status_code == 200:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=400)

        if response.status_code == -401:
            return JsonResponse({'message': 'INVALID_KAKAO_USER'}, status=400)
        
        return response.json()

