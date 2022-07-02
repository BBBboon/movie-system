from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve
from system import views

urlpatterns = [
    # re_path内部第一个是一个正则表达式，若匹配成功，serve则会对静态数据进行处理，
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 用户身份管理
    path('userid/list/', views.userid_list),
    path('userid/add/', views.userid_add),
    path('userid/delete/', views.userid_delete),
    # 传递过来的url中应该为 http://127.0.0.1:8000/depart/数字/edit/
    path('userid/<int:nid>/edit/', views.userid_edit), #为了传递nid的数值

    # 用户管理
    path('user/login/', views.user_login),
    path('user/logout/', views.user_logout),
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/modelform_add/', views.user_modelform_add),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/<int:nid>/delete/', views.user_delete),

    # 管理员管理
    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/<int:nid>/edit/', views.admin_edit),
    path('admin/<int:nid>/delete/', views.admin_delete),
    path('admin/<int:nid>/reset/', views.admin_reset),

    # 电影管理
    path('admin/movie/list/', views.admin_movie_list),
    path('admin/movie/add/', views.admin_movie_add),
    path('movies/add/multi/', views.movies_add_multi),
    path('admin/movie/<int:nid>/edit/', views.admin_movie_edit),
    path('admin/movie/<int:nid>/delete/', views.admin_movie_delete),

    # 电影
    path('home/', views.home), #主页
    path('movies/info/', views.movies_info), #所有电影信息的排行榜
    path('movies/comments/', views.movies_comments), #所有电影评论的排行榜
    path('movies/charts/', views.movies_charts), #所有电影图表的排行榜
    path('movie/<int:mid>/info/', views.movie_info), #一部电影信息
    path('movies/totalcharts/', views.movies_totalcharts), #所有电影的汇总表
    path('movie/<int:mid>/comments/', views.movie_comments), #一部电影的评论
    path('movie/<int:mid>/comment/add/', views.movie_comment_add), #发表评论
    path('movie/<int:mid>/chart/', views.movie_chart), #一部电影的图表

    # 登录
    path('login/', views.login),
    path('logout/', views.logout),
    path('image/code/', views.image_code),

    # 用户上传问题
    path('upload/problem/', views.upload_problem),
    path('problem/list/', views.problem_list),
    path('problem/<int:nid>/delete/', views.problem_delete),
]
