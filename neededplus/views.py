import datetime
from datetime            import timedelta

from django.views        import View
from django.http         import JsonResponse

from users.models        import User, SocialLogin
from neededplus.models   import NeededPlus
from core.utils          import authorization

class NeededPlusSubscription(View):
    @authorization
    def get(self, request):
        try:
            user = User.objects.get(social_login=request.user)

            return JsonResponse({"message" : "SUCCESS" ,"result" : user.is_subscription}, status = 200)

        except User.DoesNotExist:
            return JsonResponse({"message" : "DOES_NOT_EXIST_USER"}, status = 404)
        
    @authorization
    def patch(self, request):
        try:    
            user = User.objects.get(social_login=request.user)            
            
            if not user.is_subscription:
                user.is_subscription   = True
                user.subscription_date = datetime.date.today()
                user.save()
            else:
                return JsonResponse({"message" : "ALREADY_SUBSCRIBED"}, status = 400)
            
            return JsonResponse({"message" : "SUCCESS", "result" : user.subscription_date}, status = 200)

        except User.DoesNotExist:
            return JsonResponse({"message" : "DOES_NOT_EXIST_USER"}, status = 404)
