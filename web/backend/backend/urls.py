from django.urls import path, include
from . import views


#   网址 =>  urls  =>  views  =>   html
urlpatterns = [
    path('api/', include('api.urls')),
    path('', views.index, name='index'),      # 空地址等于调用index → 跑去views视图函数找登录页
    path('main/', views.main, name='main'),   # 新增：大盘页面
    path('processed/videos/<path:path>', views.serve_processed),
]