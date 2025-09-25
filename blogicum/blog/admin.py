from django.contrib import admin

from .models import Category, Location, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'created_at',
        'category',
        'location',
        'author',
        'pub_date')
    list_filter = ('is_published', 'location', 'category')
    date_hierarchy = 'pub_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author',
                    'post',
                    'text',
                    'created_at')
    list_filter = ('post', 'author')
    search_fields = ('text', 'author__username', 'post__title')
    date_hierarchy = 'created_at'
