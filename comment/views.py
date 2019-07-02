from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from comment.forms import CommentForm
from comment.models import Comment


def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('blog:index'))
    comment_form = CommentForm(request.POST, user=request.user)

    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()

        data = {
            'status': 'SUCCESS',
            'username': comment.user.username,
            'comment_time': comment.comment_time.strftime('%Y-%m-%d %H:%M:%S'),
            'text': comment.text,
        }
    else:
        data = {
            'status': 'ERROR',
            'message': list(comment_form.errors.values())[0][0]
        }

    return JsonResponse(data)




