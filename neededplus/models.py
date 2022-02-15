from django.db   import models
from core.models import TimeStampModel

class NeededPlus(TimeStampModel):
    title             = models.CharField(max_length=50)
    needed_plus_image = models.CharField(max_length=50)
    period            = models.CharField(max_length=50)

    class Meta:
        db_table = 'needed_plus'