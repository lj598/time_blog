from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    liked_num = models.IntegerField(default=0)#点赞数
    class Meta():
        db_table = 'LikeCount'

class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User,on_delete=models.CASCADE)#记录点赞人
    liked_time = models.DateTimeField(auto_now_add=True)

    class Meta():
        db_table = 'LikeRecord'
