from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    return HttpResponse('首页')


def book(request):
    return HttpResponse('book')