import datetime

from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone

from blog.forms import LoginForm, RegisterForm, BlogForm, BlogTypeForm
from blog.models import Blog, BlogType
from comment.forms import CommentForm
from comment.models import Comment
from echo_valley.settings import PAGE_NUM
from read_statistics.utils import read_statistics, week_statistic_data, read_hot_today


def read_hot_week():
    today = timezone.now().date()
    seven_days_ago = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=seven_days_ago) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:3]


def common(request, blog_list=Blog.objects.all()):  # 默认为空不知道有没有问题
    paginator = Paginator(blog_list, PAGE_NUM)  # Show 4 blogs per page
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    # 统计按年月分的博客数
    blog_date_list = Blog.objects.dates('create_time', 'month', order='DESC')
    blog_date_dict = {}
    for blog_date in blog_date_list:
        blog_date_dict[blog_date] = Blog.objects. \
            filter(create_time__year=blog_date.year, create_time__month=blog_date.month).count()

    # 统计一周的博文访问量
    content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = week_statistic_data(content_type)  # 一周数据

    # 设置缓存
    read_hot_week_blogs = cache.get("read_hot_week_blogs")
    if read_hot_week_blogs is None:
        read_hot_week_blogs = read_hot_week()
        cache.set('read_hot_week_blogs', read_hot_week(), 3600)
    else:
        print('use cache')

    context = {
        'blogs': blogs,
        'count': paginator.count,
        'blog_type_list': BlogType.objects.annotate(blog_count=Count('blog')),
        'blog_date_dict': blog_date_dict,
        'read_nums': read_nums,  # 一周数据
        'dates': dates,  # 对应日期
        'read_hot_today_datas': read_hot_today(content_type),
        'read_hot_week_blogs': read_hot_week_blogs,
    }
    return context


def index(request):
    return render(request, 'blog/index.html')


def blog(request):
    context = common(request)
    return render(request, 'blog/blog.html', context)  # render_to_response改为render时要加request


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    # 阅读数统计
    read_cookie_key = read_statistics(request, blog)

    # 上一篇下一篇
    previous_page = Blog.objects.filter(create_time__gt=blog.create_time).last()
    next_page = Blog.objects.filter(create_time__lt=blog.create_time).first()

    # 获取评论对象
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)

    context = {
        'blog': blog,
        'previous_page': previous_page,
        'next_page': next_page,
        'comments': comments,
        'comment_form': CommentForm(initial={'content_type': blog_content_type.model, 'object_id': pk}),
    }
    context.update(common(request))
    response = render(request, 'blog/detail.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response


def blog_with_tag(request, tag_id):
    blog_type = get_object_or_404(BlogType, pk=tag_id)
    # blog_type = get_object_or_404(BlogType, pk=tag_id),   该死的逗号，，，，，，，
    blog_list = Blog.objects.filter(blog_type=blog_type)

    context = {
        'blog_type': blog_type,
    }
    context.update(common(request, blog_list=blog_list))
    return render(request, 'blog/blog_with_tag.html', context)


def blog_with_data(request, year, month):
    blog_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    date = datetime.date(year=year, month=month, day=1)
    context = {
        'date': date
    }
    context.update(common(request, blog_list=blog_list))
    return render(request, 'blog/blog_with_data.html', context)


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from'), reverse('blog:index'))
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    return render(request, 'blog/login.html', context)


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            user = User.objects.create(username=username, email=email, password=password)
            user.save()
            user = auth.authenticate(username=user.username, password=request.POST['password'])
            auth.login(request, user)
            return redirect(request.GET.get('from'), reverse('blog:index'))
    else:
        register_form = RegisterForm()
    context = {
        'register_form': register_form
    }
    return render(request, 'blog/register.html', context)


def logout_view(request):
    """注销"""
    logout(request)
    return HttpResponseRedirect(reverse('blog:index'))


def new_blog(request):
    """添加新博客"""
    if request.method != 'POST':

        # 未提交数据：创建一个新表单
        blog_form = BlogForm()
    else:
        # POST提交的数据，对数据进行处理
        blog_form = BlogForm(data=request.POST)
        if blog_form.is_valid():
            new_blog = blog_form.save(commit=False)
            new_blog.author = request.user
            new_blog.save()
            return HttpResponseRedirect(reverse('blog:blog'))

    context = {
        'blog_form': blog_form,
        'type_form': new_tag(request),
    }
    return render(request, 'blog/new_blog.html', context)


def new_tag(request):
    if request.method != 'POST':

        # 未提交数据：创建一个新表单
        type_form = BlogTypeForm()
    else:
        # POST提交的数据，对数据进行处理
        type_form = BlogTypeForm(data=request.POST)
        if type_form.is_valid():
            new_type = type_form.save(commit=False)
            # new_blog.author = request.user
            new_type.save()
            return HttpResponseRedirect(reverse('blog:new_blog'))
    return type_form


def edit_blog(request, pk):
    """编辑条目"""
    blog = Blog.objects.get(id=pk)
    # if blog.author != request.user: raise Http404
    if request.method != 'POST':

        # 未提交数据：创建一个新表单
        form = BlogForm(instance=blog)
    else:
        # POST提交的数据，对数据进行处理
        form = BlogForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:detail', args=[pk]))
    context = {'blog': blog, 'form': form}
    return render(request, 'blog/edit_blog.html', context)
