# !/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :2019/6/21 17:02
# @Author  :Noperx
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.blog, name='blog'),
    path('list/<page>/', views.blog, name='blog'),
    path('<int:pk>/detail/', views.blog_detail, name='detail'),
    path('tag/<int:tag_id>/', views.blog_with_tag, name='blog_with_tag'),
    path('<int:year>/<int:month>/', views.blog_with_data, name='blog_with_data'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('new_blog/', views.new_blog, name='new_blog'),
    path('new_tag/', views.new_tag, name='new_tag'),
    path('edit_blog/<int:pk>/', views.edit_blog, name='edit_blog'),
]