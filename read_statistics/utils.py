# !/usr/bin/env python
# _*_coding:utf-8 _*_
# @Time    :2019/6/27 16:47
# @Author  :Noperx
import datetime

from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone

from read_statistics.models import ReadNum, ReadDetail


def read_statistics(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        readnum, create = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        date = timezone.now().date()
        readDetail, create = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key


def week_statistic_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return read_nums, dates


def read_hot_today(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details


# def read_hot_week(content_type):
#     today = timezone.now().date()
#     seven_days_ago = today - datetime.timedelta(days=7)
#     read_details = ReadDetail.objects\
#                                     .filter(content_type=content_type, date__lt=today, date__gte=seven_days_ago)\
#                                     .values('content_type', 'object_id')\
#                                     .annotate(read_num_sum=Sum('read_num'))\
#                                     .order_by('-read_num_sum')
#     return read_details[:3]


def read_hot_month():
    pass