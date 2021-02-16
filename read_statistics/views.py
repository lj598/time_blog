from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_day#引入方法
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)#获取博客
    dates,read_nums = get_seven_days_read_data(blog_content_type)#得到博客的前七天阅读数据
    today_hot_day = get_today_hot_data(blog_content_type)
    # yesterday_hot_day = get_yesterday_hot_day(blog_content_type)
    #获取昨天热门博客缓存数据
    yesterday_hot_day = cache.get('yesterday_hot_day')
    if yesterday_hot_day is None:
        yesterday_hot_day = get_yesterday_hot_day(blog_content_type)#如果数据为空则调用方法获取数据
        cache.set('yesterday_hot_day',yesterday_hot_day,3600)#以秒为单位，由于昨天的数据已经确定，不需要实时获取
        print("computing cache")
    else:
        print("use cache")

    #seven_hot_day = get_7_days_hot_blogs()
    context = {}
    context['dates'] = dates#所有数据都要有这种格式返回，前端才能获取数据
    context['read_nums'] = read_nums
    context['today_hot_day'] = today_hot_day
    context['yesterday_hot_day'] = yesterday_hot_day
    #context['seven_hot_day'] = seven_hot_day
    return dates,read_nums,today_hot_day,yesterday_hot_day
    #return render(request,'registic.html',context)#将获取的数据返回到博客列表，之后在前端安排位置



