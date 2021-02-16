from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.login,name='login'),#登陆方法
    path('login_out/',views.login_out,name='login_out'),#这是退出登陆的方法
    path('user_info/',views.user_info,name='user_info'),#用户信息页
    path('registic/',views.registic,name='registic'),#注册方法
    path('change_nickname/',views.change_nickname,name='change_nickname'),
    path('change_password/',views.change_password,name='change_password'),
    path('change_email/',views.change_email,name='change_email'),
    path('send_verification/',views.send_verification,name='send_verification'),
]