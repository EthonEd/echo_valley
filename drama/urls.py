# !/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :2019/6/20 22:50
# @Author  :Noperx

from . import  views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index')
]