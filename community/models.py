from django.db   import models
from core.models import TimeStampModel

class Comment(TimeStampModel):
    content = models.CharField(max_length=200)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    post    = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')

    class Meta:
        db_table = 'comments'

class Post(TimeStampModel):
    title              = models.CharField(max_length=50)
    content            = models.CharField(max_length=500)
    community_category = models.ForeignKey('CommunityCategory', on_delete=models.CASCADE, related_name='posts')

    class Meta:
        db_table = 'posts'

class CommunityCategory(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'community_categories'

class Like(TimeStampModel):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='likes')

    class Meta:
        db_table = 'likes'
