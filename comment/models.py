from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.
class Comment(models.Model):#创建评论表模型
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)  # 可通过ContentType找到对应的博客类型
    object_id = models.PositiveIntegerField()  # 记录对应模型的主键值
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField()#评论内容
    comment_time = models.DateTimeField(auto_now_add=True)#评论时间
    user = models.ForeignKey(User,related_name="comments",on_delete=models.DO_NOTHING)#用户,利用一个User关联外键
    #表示这条评论是user写的
    root = models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.DO_NOTHING)
    #利用树结构，一条评论对应一条至多条回复

    parent = models.ForeignKey('self',related_name='parent_comment',null=True,on_delete=models.DO_NOTHING)#利用一个外键
    reply_to = models.ForeignKey(User,related_name="replies",null=True,on_delete=models.DO_NOTHING)#表示这条回复是给谁的评论回复

    def __str__(self):
        return self.text#转换为评论内容
    class Meta:
        db_table = "comment"
        ordering = ['-comment_time']#按评论时间倒叙排序

#class Reply(models.Model):#回复模型
    #comment = models.ForeignKey(Comment,on_delete=models.DO_NOTHING)#找到对应的评论，实现评论可被回复










