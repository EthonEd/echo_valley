from django.contrib import admin
from .models import BlogType, Blog

# Register your models here.


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']
    # inlines = [BlogAdmin]


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # model = BlogType
    # extra = 1
    # fieldsets = [
    #     (None,               {'fields': ['title']}),
    #     ('Date information', {'fields': ['create_time', 'last_update_time'], 'classes': ['collapse']}),
    #     ('foreign key',      {'fields': ['blog_type', 'author']})
    # ]
    list_display = ('title', 'blog_type', 'author', 'get_read_num', 'create_time', 'last_update_time')


# admin.site.register(Blog, BlogType, BlogAdmin, BlogAdmin)
