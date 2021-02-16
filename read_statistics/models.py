from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone#当天日期
# Create your models here.
class ReadNum(models.Model):#计数模型
    read_num = models.IntegerField(default=0)#计数字段
    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)#可通过ContentType找到对应的博客类型
    object_id = models.PositiveIntegerField()#记录对应模型的主键值
    content_object = GenericForeignKey('content_type','object_id')
    class Meta():
        db_table = 'readnum'

class ReadDetail(models.Model):#记录日期信息
    date = models.DateField(default=timezone.now)#记录当天日期
    read_num = models.IntegerField(default=0)#记录阅读数
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)  # 可通过ContentType找到对应的博客类型
    object_id = models.PositiveIntegerField()  # 记录对应模型的主键值
    content_object = GenericForeignKey('content_type', 'object_id')
    class Meta():
        db_table = 'readdetail'

class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0




