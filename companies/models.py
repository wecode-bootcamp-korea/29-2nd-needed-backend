from django.db   import models
from core.models import TimeStampModel

class Company(TimeStampModel):
    name        = models.CharField(max_length=45)
    description = models.URLField(max_length=1000)
    detail_area = models.ForeignKey('DetailArea', on_delete=models.CASCADE, related_name='companys')

    class Meta:
        db_table = 'companies'

class CompanyImage(TimeStampModel):
    image_url = models.URLField(max_length=500)
    company   = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='company_images')

    class Meta:
        db_table = 'company_images'

class Country(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'countries'

class Province(models.Model):
    name    = models.CharField(max_length=45)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='provinces')

    class Meta:
        db_table = 'provinces'

class DetailArea(models.Model):
    name     = models.CharField(max_length=45)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, related_name='detail_areas')

    class Meta:
        db_table = 'detail_areas'

class TagCompany(TimeStampModel):
    tag     = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='tag_companies')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='tag_companies')

    class Meta:
        db_table = 'tag_companies'

class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tags'