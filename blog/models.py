from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone#当天日期
from ckeditor_uploader.fields import RichTextUploadingField#引入可添加图片的富文本编辑器
from read_statistics.models import ReadNumExpandMethod

# Create your models here.

class BlogType(models.Model):
    type_name = models.CharField(max_length=16)
    def __str__(self):
        return self.type_name
    class Meta():
        db_table = 'BlogType'

class Blog(models.Model,ReadNumExpandMethod):
    title = models.CharField(max_length=32)#标题
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING,related_name='blog_type')
    content = RichTextUploadingField()#写博客正文
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)#自动添加提交时间
    last_updated_time = models.DateTimeField(auto_now=True)
    comments_num = models.IntegerField(default=0)
    #阅读计数方法2
    def __str__(self):
        return "<Blog:%s>" % self.title#这一动作是为了在后台管理中显示博客管理的内容
    class Meta():
        db_table = 'Blog'
        ordering = ['-created_time']#降序

class Message_board(models.Model):
    message = models.TextField(default='')
    message_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    class Meta():
        db_table = 'Message_board'

class Resgistic(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    email = models.CharField(max_length=16)
    created_time = models.DateTimeField(auto_now_add=True)
