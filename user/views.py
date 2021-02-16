from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from .models import Profile
import string
import random

# Create your views here.

def login(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(request,username=username,password=password)
    #referer = request.META.get('HTTP_REFERER')#登录前所在的页面,后面的是别名解析，返回到首页
    # referer = re.sub('load_login/[?]from=/','',referer)#修改重定向的地址
    if user is not None:
        auth.login(request,user)
        return redirect(request.GET.get('from',reverse('home')))
    # elif User.objects.filter(email=username).exists() :
    #     get_username = User.objects.get(email=username).username#通过邮箱获取用户的用户名
    #     user = auth.authenticate(request,username=get_username, password=password)
    #     auth.login(request,user)
    #     return redirect(request.GET.get('from', reverse('home')))
    else:
        return render(request,'error.html',{'message':"用户名或密码错误"})

def registic(request):
    username = request.POST.get('username','')
    password = request.POST.get('password', '')
    re_password = request.POST.get('re_password', '')
    email = request.POST.get('email','')
    if User.objects.filter(username=username).exists():
        return render(request,'error.html',{'message':"用户名已存在，请重新输入"})
    if password != re_password:
        return render(request,'error.html',{'message':"两次输入的密码不一致，请检查"})
    if username=="" or password=="" or email =="":
        return render(request,'error.html',{'message':"信息不完整"})
    #注册操作
    user = User.objects.create_user(username,email,password)#在user模板写入这三个数据
    user.save()
    # user = User()#这是第二中方法注册
    # user.username=username
    # user.email=email
    # user.set_password(password)#添加加密后的密码
    # user.save()
    #注册完直接登录用户
    user = auth.authenticate(request, username=username, password=password)
    auth.login(request, user)
    return redirect(request.GET.get('from', reverse('home')))

def login_out(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    context = {}
    return render(request,'user_info.html',context)

def change_nickname(request):
    context = {}
    if request.method == 'POST':
        new_nickname = request.POST.get('nickname')
        if new_nickname == '':
            context['error'] = "昵称不能为空"
            return render(request,'user_info.html',context)
        Profile.objects.get_or_create(user=request.user)#这句不能漏
        profile_a = Profile.objects.get(user=request.user)
        profile_a.nickname = new_nickname
        profile_a.save()
    return redirect(request.GET.get('from', reverse('user_info')))

def change_password(request):
    context = {}
    if request.method == 'POST':
        pe_password = request.POST.get('pe_password')
        new_password = request.POST.get('new_password')
        if pe_password  == '' or new_password == '':
            context['pass_error'] = "密码不能为空"
            return render(request,'user_info.html',context)
        user = User.objects.get(id=request.user.id)
        if not user.check_password(pe_password):
            context['pass_error'] = "原始密码不正确"
            return render(request, 'user_info.html', context)
        user.set_password(new_password)
        user.save()
        #user_info = auth.authenticate(request,username=request.user.username,password=new_password)
        #auth.login(request,user_info)#这边是修改密码后自动重新登录
        auth.logout(request)#这边是修改密码后自动登出
        return redirect(request.GET.get('from', reverse('home')))
    return redirect(request.GET.get('from', reverse('user_info')))

def change_email(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        verification = request.POST.get('verification')
        localcode = request.session['bind_email_code']
        if User.objects.filter(username=request.user.username,email=email).exists():
            context['status'] = "邮箱重复"
            return render(request,'user_info.html',context)
        #获取邮箱和验证码,验证码和服务器生成的验证码对比，如果相同则将提交的邮箱写入数据库
        if verification != localcode:
            context['status'] = "验证码错误"
            return render(request, 'user_info.html', context)
        request.user.email = email
        request.user.save()
        del request.session['bind_email_code']
    return redirect(request.GET.get('from', reverse('user_info')))

def send_verification(request):#生成验证码并发送
    email = request.POST.get('email','')
    data = {}
    if email != '':
        #生成随机验证码
        verification = random.sample(string.ascii_letters,5)#随机生成大小写组合的5位验证码
        code = ''.join(verification)#转换为字符串
        request.session['bind_email_code'] = code
        #发送验证码
        send_mail(
            '绑定邮箱需要进行身份验证',
            '验证码:%s' % code,
            '857400934@qq.com',#从何处发送过来
            [email],#接收邮件的邮箱
            fail_silently=False,#是否忽略错误
        )
        data['status'] = '发送成功!'
    else:
        data['status'] = '发生未知错误，请联系管理员!'
    return JsonResponse(data)

