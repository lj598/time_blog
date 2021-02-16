from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator#引用分页器
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from blog.models import Blog,BlogType,Message_board
from read_statistics.utils import read_statistics_once_read
from read_statistics.views import home
from comment.views import return_new_comment
from comment.form import CommentForm,Message_Form
# Create your views here.

def blog_list(request):#博客列表(首页)，集成了分页器
    blogs_all_list = Blog.objects.all()
    page_num=request.GET.get('page',1)#获取页码参数(一个GET请求)#
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER)#每5页进行一次分页#分页器
    page_of_blogs = paginator.get_page(page_num)
    blogs_type = BlogType.objects.annotate(blog_count=Count('blog_type'))#获取对应博客数量
    data = home(request)  # 方法重写，利用home方法返回两组数据，分别是阅读量和日期
    context = {}
    context['new_comments'] = return_new_comment()
    context['date'] = data[0]
    context['read_nums'] = data[1]
    context['today_hot_day'] = data[2]
    context['yesterday_hot_day'] = data[3]
    context['page_of_blogs'] = page_of_blogs
    context['blogs_type'] = blogs_type
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")#精确到当月
    return render(request,'blogs_list.html',context)

def blog_with_date(request,year,month):#按年月分类博客
    blogs_all_list = Blog.objects.filter(#获取当前年月的所有文章
        created_time__year=year,
        created_time__month=month
    )
#获取日期归档对应的博客数量
#第一种方法
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    #print(blog_dates_dict)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数#
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER)#按setting中的参数分页数#
    page_of_blogs = paginator.get_page(page_num)
    data = home(request)  # 方法重写，利用home方法返回两组数据，分别是阅读量和日期
    context = {}
    context['new_comments'] = return_new_comment()
    context['date'] = data[0]
    context['read_nums'] = data[1]
    context['today_hot_day'] = data[2]
    context['yesterday_hot_day'] = data[3]
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs#当前页
    context['blog_dates'] = blog_dates_dict
    return render(request,'blogs_list.html',context)

def blog_detail(request,blog_id):#博客内容页
    # #获取博客id
    blog = get_object_or_404(Blog, id=blog_id)
    blog_content_type = ContentType.objects.get_for_model(blog)
    read_cookie_key = read_statistics_once_read(request,blog)#读取该条博客的cookie信息
    data = home(request)  # 方法重写，利用home方法返回两组数据，分别是阅读量和日期
    context = {}
    dat = {}
    dat['content_type'] = blog_content_type.model
    dat['object_id'] = blog_id
    dat['reply_comment_id'] = 0
    context['comment_form'] = CommentForm(initial=dat)
    #context['comments_count'] = blog_f[2]#评论数
    #context['comments'] = blog_f[1]#将对应的评论返还至前端
    context['date'] = data[0]
    context['read_nums'] = data[1]
    context['today_hot_day'] = data[2]
    context['yesterday_hot_day'] = data[3]
    #context['seven_hot_day'] = data[4]
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()#搜索当前博客之前博客的最后一条(也就是当前博客的前一条)
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()#搜索当前博客之后的第一条博客(也就是当前博客的后一条)
    context['blogs'] = blog#这句是当前博客
    context['user']=request.user
    context['new_comments'] = return_new_comment()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")#精确到当月
    #context['readed_num'] = blog.readed_num#博客阅读次数
    response = render(request,'blogs_detail.html',context)#响应
    response.set_cookie(read_cookie_key,'true',max_age=30)#阅读cookie标记,设置30秒内有效
    return response

def blog_with_type(request,blog_type_id):#按类型分类
    blog_type_name = get_object_or_404(BlogType, pk=blog_type_id)
    blog = Blog.objects.filter(blog_type=blog_type_name)
    blogs_type = BlogType.objects.annotate(blog_count=Count('blog_type'))  # 获取对应博客数量
    page_num = request.GET.get('page', 1)  # 获取url的页面参数#
    paginator = Paginator(blog, settings.EACH_PAGE_BLOGS_NUMBER)  # 按setting中的参数分页数#
    page_of_blogs = paginator.get_page(page_num)
    data = home(request)  # 方法重写，利用home方法返回两组数据，分别是阅读量和日期
    context = {}
    context['new_comments'] = return_new_comment()
    context['date'] = data[0]
    context['read_nums'] = data[1]
    context['today_hot_day'] = data[2]
    context['yesterday_hot_day'] = data[3]
    context['page_of_blogs'] = page_of_blogs
    context['blogs_type'] = blogs_type
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")  # 精确到当月
    return render(request,'blogs_type.html',context)

def message_block(request):#提交留言
    data = home(request)  # 方法重写，利用home方法返回两组数据，分别是阅读量和日期
    context = {}
    context['date'] = data[0]
    context['read_nums'] = data[1]
    context['today_hot_day'] = data[2]
    context['yesterday_hot_day'] = data[3]
    context['comment_form'] = CommentForm()
    context['new_comments'] = return_new_comment()
    context['message'] = Message_Form()
    referer = request.META.get('HTTP_REFERER', reverse('home'))  # 返回首页
    message_form = Message_Form(request.POST)

    if message_form.is_valid():
        message = Message_board()
        # print(message)
        message.message = message_form.cleaned_data['text']
        print(message.message)#带标签
        message.save()
        context = {
            'success': '留言提交成功'
        }
        return render(request,'message_block.html',context)
    return render(request,'message_block.html',context)

def index(request):#测试页
    data = home(request)  # 方法重写，利用home方法返回多组数据
    context = {}
    context['date'] = data[0]
    context['read_nums'] = data[1]
    context['today_hot_day'] = data[2]
    context['yesterday_hot_day'] = data[3]
    context['new_comments'] = return_new_comment()#只返回最新的前三条,且倒序返回
    #context['seven_hot_day'] = data[4]
    return render(request,'index.html',context)

def search(request):#站内搜索
    keyword = request.POST.get('search')#从前端获取搜索内容
    print(keyword)
    list = Blog.objects.all()#选取全部博客
    searchResult = []
    for x in list:
        if keyword in x.title:
            searchResult.append(x)
    searchResult = set(searchResult)
    print("=============")
    print(type(list))
    print("搜索结果:",searchResult)
    print("所有博客:",list)
        # try:
        #     blog_data1 = Blog.objects.get(title=search_text)
        #     blog_data2 = Blog.objects.get(blog_type=search_text)
        # except:
        #     context = {
        #         'error':"没有找到相关的博客文章"
        #     }
        #     return render(request,'blogs_list.html',context)

    #这里对搜索的内容分页
    blogs_list = Blog.objects.all()
    page_num = request.GET.get('page', 1)  # 获取页码参数(一个GET请求)#
    paginator = Paginator(blogs_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每5页进行一次分页#分页器
    page_of_blogs = paginator.get_page(page_num)
    # BlogType.objects.annotate(blog_count=Count('blog_type_key'))
    blogs_type = BlogType.objects.annotate(blog_count=Count('blog_type'))  # 获取对应博客数量
    print(blogs_type)
    data = home(request)  # 方法重写，利用home方法返回两组数据，分别是阅读量和日期
    context = {}
    context['new_comments'] = return_new_comment()
    context['date'] = data[0]
    context['read_nums'] = data[1]
    context['today_hot_day'] = data[2]
    context['yesterday_hot_day'] = data[3]
    # context['seven_hot_day'] = data[4]
    # print(data[2])
    context['page_of_blogs'] = page_of_blogs
    # context['blogs_type'] = blogs_type#BlogType.objects.all()
    context['blogs_type'] = blogs_type
    # context['blog_dates'] = Blog.objects.dates('created_time','day',order="DESC")#精确到当天
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")  # 精确到当月
    return render(request, 'blogs_list.html',context)

def blog_photo(request):#添加照片(墙)
    return render(request,'blogs_photo.html')

def load_login(request):
    #print(referer_num)
    return render(request,'login.html')

def load_registic(request):
    return render(request,'registic.html')
