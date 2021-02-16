from django.urls import path
from blog import views
from read_statistics import views as re_views
app_name = 'blog'
urlpatterns = [
    path('index/',views.index,name="index"),
    path('blog_list/',views.blog_list,name="blog_list"),
    path('<int:blog_id>',views.blog_detail,name="blog_detail"),
    path('type/<blog_type_id>/',views.blog_with_type,name = "blog_with_type"),
    path('date/<int:year>/<int:month>',views.blog_with_date,name="blog_with_date"),
    path('message_block/',views.message_block,name="message_block"),
    path('search/',views.search,name="search"),
    path('photo/',views.blog_photo,name="photo"),
    path('home/',re_views.home,name="home"),
    path('load_login/',views.load_login,name="load_login"),#进入登陆页面的方法
    path('load_registic/',views.load_registic,name="load_registic")
]