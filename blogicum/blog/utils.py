from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Post, Comment


def get_base_post():
    """Возвращает базовый queryset опубликованных постов."""
    return Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')


def get_paginated_post(request, queryset, per_page):
    """Создает пагинацию для queryset постов."""
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def get_post_queryset():
    """Возвращает оптимизированный queryset постов с select_related и annotate."""
    return Post.objects.select_related('author',
                                       'category',
                                       'location').annotate(
                                           comment_count=Count('comments')
    )


def optimize_post_queryset(queryset):
    """Оптимизирует queryset постов с select_related и annotate."""
    return queryset.select_related('author', 'category', 'location').annotate(
        comment_count=Count('comments')
    )


def get_post_for_detail(post_id, user=None):
    """Получает пост для детального просмотра с учетом прав доступа."""
    # Сначала пытаемся найти опубликованный пост
    post = get_post_queryset().filter(
        id=post_id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).first()
    
    # Если не найден опубликованный пост и пользователь авторизован,
    # проверяем, может ли он видеть свой неопубликованный пост
    if not post and user and user.is_authenticated:
        post = get_post_queryset().filter(
            id=post_id,
            author=user
        ).first()
    
    return post


def get_post_comments(post):
    """Получает комментарии к посту с оптимизацией."""
    return (
        Comment.objects.filter(post=post)
        .select_related('author')
        .order_by('created_at')
    )