from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from mdeditor.fields import MDTextField

from read_statistics.models import UtilMethod, ReadDetail


class Author(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name


class BlogType(models.Model):
    type_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.type_name


class Blog(models.Model, UtilMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    # content = models.TextField()
    # content = RichTextField()
    content = MDTextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    read_details = GenericRelation(ReadDetail)
    
    def __str__(self):
        return '<Blog: %s>' % self.title

    class Meta:
        ordering = ['-create_time']




