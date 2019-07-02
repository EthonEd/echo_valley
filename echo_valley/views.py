# !/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :2019/6/21 17:37
# @Author  :Noperx
from django.http import HttpResponse


def index(request):
    return HttpResponse('主页面开发中，敬请期待...')