import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from .models import ReadNum,ReadDetail

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model,obj.pk)
    if not request.COOKIES.get(key):  # 当不存在该cookie时
        readnum,created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        date = timezone.now().date()#提取当天的日期
        readDetial,created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        readDetial.read_num+=1
        readDetial.save()
    return key

def get_seven_days_read_data(content_type):#取各种类型的阅读数据
    today = timezone.now().date()#获取当天的阅读数据
    # today - datetime.timedelta(days=1)#today的前一天
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)#today的前七天
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type,date=date)#获取前七天的阅读数据
        result = read_details.aggregate(read_num_sum = Sum('read_num'))#对read_num字段进行求和
        read_nums.append(result['read_num_sum'] or 0)
    return dates,read_nums

def get_today_hot_data(content_type):#传入一个博客类型
    today = timezone.now().date()  # 获取当天的阅读数据
    read_details = ReadDetail.objects.filter(content_type=content_type,date=today)#在ReadDetail表查询当天的浏览记录，将查询结果放在read_details里面
    read_details = read_details.order_by('-read_num')#博客阅读量由大到小排序排行
    return read_details[:5]

def get_yesterday_hot_day(content_type):#和上一个方法一样
    today = timezone.now().date()
    yesterday = today-datetime.timedelta(days=1)#减去一天
    read_details = ReadDetail.objects.filter(content_type=content_type,date=yesterday)
    read_details = read_details.order_by('-read_num')#博客阅读量由大到小排序排行
    print(read_details)
    return read_details[:5]






