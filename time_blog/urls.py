"""time_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from blog import views

urlpatterns = [
    path('',views.blog_list,name='home'),#设置博客列表页为首页
    path('',include('blog.url',namespace='blog'),name='home'),#这句方便前端使用后端的接口
    path('index/',views.index),#测试页，这一页作为base(后面可删掉这句)
    path('admin/', admin.site.urls),
    path('comment/',include('comment.url')),
    path('likes/',include('likes.url')),
    path('user/',include('user.url')),
    path('ckeditor',include('ckeditor_uploader.urls')),#上传图片的url
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

