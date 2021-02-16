from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from .models import LikeCount,LikeRecord
# Create your views here.
def ErrorResponse(code,message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def like_change(request):
    user = request.user
    if not user.is_authenticated:  # 如果没有登录,则不能点赞
        return ErrorResponse(400, '暂未登录,请登陆后再点赞')

    get_content_type = request.GET.get('content_type')#文章类型
    object_id = request.GET.get('object_id')#博客id
    try:
        content_type = ContentType.objects.get(model=get_content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
        print("model_obj:",model_obj)
    except ObjectDoesNotExist:
        return ErrorResponse(401,'对象不存在')

    is_like = request.GET.get('is_like')
    print("user:",user)#admin
    print("content_type:",content_type)#blog
    print("object_id:",object_id)#id
    print("is_like:",is_like)#false
    print("==============")

    #登录后尝试点赞
    like_record = LikeRecord.objects.filter(content_type=content_type,object_id=object_id,user=user).exists()

    print("bool_like_record:",like_record)#未创建，显示false
    if like_record == False:
        #进行点赞操作，创建点赞记录
        like_record = LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)
        like_count = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
        like_num = LikeCount.objects.get(object_id=object_id)
        like_num.liked_num +=1
        like_num.save()
        print("like_num:",like_num)
        print("like_record:",like_record)
        return SuccessResponse(like_num.liked_num)#保存点赞记录和点赞数，返回点赞数
    else:#点赞功能直接做成不能取消的方式
        return ErrorResponse(402,'已经点赞,不能取消点赞')#已经点赞而不能够再次点赞，直接返回一个已点赞的错误
    #like_record = LikeRecord.objects.get_or_create(object_id=object_id,content_type=content_type,user=user)
    #print(like_record)
