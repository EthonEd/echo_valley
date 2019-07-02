# !/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :2019/6/28 9:09
# @Author  :Noperx
from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.book, name='book'),
    path('list/<page>/', views.book, name='book'),
]