from enum        import Enum

from django.db   import models

from core.models import TimeStampModel, SoftDeleteModel

class OccupationCategory(TimeStampModel):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'occupation_categories'

class OccupationSubcategory(TimeStampModel):
    name                = models.CharField(max_length=50)
    occupation_category = models.ForeignKey('OccupationCategory', on_delete=models.CASCADE, related_name='occupation_subcategories')
    
    class Meta:
        db_table = 'occupation_subcategories'

class Recruitment(TimeStampModel):
    name                   = models.CharField(max_length=50)
    description            = models.TextField(max_length=2000)
    occupation_subcategory = models.ForeignKey('OccupationSubcategory', on_delete=models.CASCADE,related_name='recruitments')
    company                = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='recruitments')
    deadline               = models.DateField()
    compensation           = models.PositiveIntegerField()
    address                = models.CharField(max_length=200)           

    class Meta:
        db_table = 'recruitments'

class Application(TimeStampModel, SoftDeleteModel):
    user               = models.ForeignKey('users.SocialLogin', on_delete=models.CASCADE, related_name='applications')
    recruitment        = models.ForeignKey('Recruitment', on_delete=models.CASCADE, related_name='applications')
    application_status = models.ForeignKey('ApplicationStatus', on_delete=models.CASCADE, related_name='applications')
    
    class Meta:
        db_table = 'applications'

class ResumeApplication(TimeStampModel):
    application = models.ForeignKey('Application', on_delete=models.CASCADE, related_name='resume_applications')
    resume      = models.ForeignKey('resumes.Resume', on_delete=models.CASCADE, related_name='resume_applications')
    
    class Meta:
        db_table = 'resume_applications'


class ApplicationStatus(TimeStampModel):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'application_statuses'

class Bookmark(TimeStampModel):
    recruitment = models.ForeignKey('Recruitment', on_delete=models.CASCADE, related_name='bookmarks')
    user        = models.ForeignKey('users.SocialLogin', on_delete=models.CASCADE, related_name='bookmarks')

    class Meta:
        db_table = 'bookmarks'
        
class ApplicationEnum(Enum):
    APPLICATION_COMPLETE = 1
    ACCEPTED_DOCUMENT    = 2
    FINAL_ACCEPTANCE     = 3
    FAIL_ACCEPTANCE      = 4
    