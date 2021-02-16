from django import template
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.form import CommentForm
from blog.models import Blog
register = template.Library()
@register.simple_tag#注册的模板标签，可用在模板页面，使用前需引用
def get_comment_count(object):#输入一个博客
    content_type = ContentType.objects.get_for_model(object)#通过model或者model的实例来寻找ContentType类型
    print(content_type)
    #con = ContentType.objects.get_for_id()#通过id寻找ContentType类型
    comment_count = Comment.objects.filter(content_type=content_type,object_id=object.pk).count()
    return comment_count#返回评论数

@register.simple_tag
def get_comment_list(object):
    content_type = ContentType.objects.get_for_model(object)
    comments = Comment.objects.filter(content_type=content_type,object_id=object.pk,parent=None)
    return comments.order_by('-comment_time')









