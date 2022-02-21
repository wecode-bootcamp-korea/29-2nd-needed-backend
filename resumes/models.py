from django.db   import models
from core.models import TimeStampModel

class Resume(TimeStampModel):
    document = models.URLField(max_length=500)
    user     = models.ForeignKey('users.SocialLogin', on_delete=models.CASCADE, related_name='resumes')
    
    class Meta:
        db_table = 'resumes'
