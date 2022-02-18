from enum        import Enum
from django.db   import models
from core.models import TimeStampModel

class User(TimeStampModel):
    phone_number    = models.CharField(max_length=100, null=True)
    address         = models.CharField(max_length=100, null=True)
    career          = models.PositiveIntegerField(null=True)
    salary          = models.PositiveIntegerField(null=True)
    is_subscription = models.BooleanField(default=False)
    social_login    = models.ForeignKey('SocialLogin', on_delete=models.CASCADE, related_name='users')
    class Meta:
        db_table = 'users'

class SocialCompany(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'social_companies'

class SocialLogin(TimeStampModel):
    email                 = models.EmailField(null=True)
    name                  = models.CharField(max_length=45)
    profile_image         = models.URLField(max_length=500, null=True)
    identification_number = models.CharField(max_length=500)
    social_company        = models.ForeignKey('SocialCompany', on_delete=models.CASCADE, related_name='social_login')
    class Meta:
        db_table = 'social_logins'

class SocialCompanyEnum(Enum):
    KAKAO  = 1
    GOOGLE = 2
    NAVER  = 3
    APPLE  = 4
