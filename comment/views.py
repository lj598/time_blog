from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Comment
from .form import CommentForm
from django.utils import timezone#当天日期

def return_new_comment():#返回最新评论
    now = timezone.now()
    two_hours_yet = now - timezone.timedelta(hours=2)  # 正确地返回了两个小时前
    #print(two_hours_yet)
    new_comments = Comment.objects.filter(comment_time__lte=now,comment_time__gte=two_hours_yet)
    print(new_comments[:3])
    context = {}
    context['new_comments'] = new_comments[:3]  # 只返回最新的前三条
    return context['new_comments']

def update_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    data = {}
    #数据检查
    if not request.user.is_authenticated:#判断登陆状态
        return render(request,'error.html',{'message':'用户未登录!','redirect_to':referer})
    text = request.POST.get('text','').strip()#以前端模板的"name"字段获取内容
    if text == "":
        return render(request,'error.html',{'message':'评论内容不能为空!','redirect_to':referer})
    try:
        content_type = request.POST.get('content_type', '')  # 如果获取为空则返回一个""内容
        object_id = int(request.POST.get('object_id', ''))  # 获取id，并转为整型数值
        model_class = ContentType.objects.get(model=content_type).model_class()  # 获取具体的模型
        model_obj = model_class.objects.get(pk=object_id)  # 获取的是博客的title
        # print(content_type)  # 获取类型，这里获取的是博客
        # print(object_id)  # 博客的id
        # print(model_class)  # <class 'blog.models.Blog'>
        # print(model_obj)  # <Blog:title>
    except Exception as e:
        return render(request,'error.html',{'message':'评论对象不存在!','redirect_to':referer})
    if comment_form.is_valid():
        comment = Comment()#实例化Comment表
        comment.user = request.user#开始写入评论数据
        comment.text = text
        comment.content_object = model_obj

        parent = comment_form.cleaned_data['parent']
        # if not parent is None:#当parent不是none的时候表示为一条回复，而不是评论
        #     comment.root = parent.root if not parent.root is None else parent#如果parent是None表示为一个顶级评论，不为none就是下级回复
        #     comment.parent = parent
        #     comment.reply_to = parent.user
        comment.save()
        # if not parent is None:
        #     data['reply_to'] = comment.reply_to.username
        # else:
        #     data['reply_to'] = ''
        # data['pk'] = comment.pk
    return redirect(referer)#返回当前博客
    #return render(request,'blogs_detail.html',data)


# def update_comment(request):#启用ajax的提交方法
#     comment_form = CommentForm(request.POST,user=request.user)
#     referer = request.META.get('HTTP_REFERER', reverse('home'))
#     data = {}
#     if comment_form.is_valid():
#         #检查通过，保存数据
#         comment = Comment()#实例化Comment表
#         comment.user = comment_form.cleaned_data['user']#开始写入评论数据
#         comment.text = comment_form.cleaned_data['text']
#         comment.content_object = comment_form.cleaned_data['content_object']
#         parent = comment_form.cleaned_data['parent']
#         if not parent is None:  # 当parent不是none的时候表示为一条回复，而不是评论
#             comment.root = parent.root if not parent.root is None else parent  # 如果parent是None表示为一个顶级评论，不为none就是下级回复
#             comment.parent = parent
#             comment.reply_to = parent.user
#         comment.save()
#
#         #返回的数据
#         data['status'] = 'SUCCESS'
#         data['username'] = comment.user.username
#         data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
#         data['text'] = comment.text
#         data['url'] = referer
#         if not parent is None:
#             data['reply_to'] = comment.reply_to.username
#         else:
#             data['reply_to'] = ''
#         data['pk'] = comment.pk
#     else:
#         #return render(request,'error.html',{'message':comment_form.errors,'redirect_to':referer})
#         data = {}
#         data['status'] = 'ERROR'
#         data['message'] = list(comment_form.errors.values())[0]
#     return JsonResponse(data)

# def test(request):
#     test1 = request.POST.get('test','')
#     data = {}
#     data['test1'] = test1
#     print(test1)
#     return JsonResponse(data)
