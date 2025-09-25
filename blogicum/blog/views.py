from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import Http404

from .constants import POSTS_ON_MAIN, POSTS_PER_PAGE
from .models import Category, Post, Comment
from .utils import (get_base_post,
                    get_paginated_post,
                    get_post_queryset,
                    optimize_post_queryset)
from .forms import PostForm, EditUserForm, CommentForm


def index(request):
    """Главная страница с опубликованными постами."""
    qs = optimize_post_queryset(get_base_post()).order_by('-pub_date')
    page_obj = get_paginated_post(request, qs, POSTS_ON_MAIN)
    return render(request, "blog/index.html", {'page_obj': page_obj})


def post_detail(request, post_id):
    """Детальная страница поста с комментариями."""
    post = get_post_queryset().filter(
        id=post_id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).first()

    # Если не найден опубликованный пост
    if not post and request.user.is_authenticated:
        post = get_post_queryset().filter(
            id=post_id,
            author=request.user
        ).first()

    if not post:
        raise Http404
    comments = (
        Comment.objects.filter(post=post)
        .select_related('author')
        .order_by('created_at')
    )
    form = CommentForm()
    return render(
        request,
        "blog/detail.html",
        {"post": post, 'comments': comments, 'form': form}
    )


def category_posts(request, category_slug):
    """Страница постов определенной категории."""
    category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
            is_published=True
        )
    )
    qs = optimize_post_queryset(
        get_base_post().filter(category=category)
    ).order_by('-pub_date')
    page_obj = get_paginated_post(request, qs, POSTS_PER_PAGE)
    return render(
        request,
        "blog/category.html",
        {'category': category, 'page_obj': page_obj})


def profile(request, username):
    """Страница профиля пользователя с его постами."""
    author = get_object_or_404(get_user_model(), username=username)
    is_owner = request.user.is_authenticated and request.user == author
    if is_owner:
        qs = (get_post_queryset()
              .filter(author=author)
              .order_by('-pub_date'))
    else:
        qs = optimize_post_queryset(
            get_base_post().filter(author=author)
        )
    page_obj = get_paginated_post(request, qs, POSTS_PER_PAGE)
    context = {
        'author': author,
        'is_owner': is_owner,
        'page_obj': page_obj,
        'profile': author,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    """Редактирование профиля пользователя."""
    form = EditUserForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})


@login_required
def create_post(request):
    """Создание нового поста."""
    form = PostForm(request.POST or None, request.FILES)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    """Редактирование существующего поста."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    """Удаление поста."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post.id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    return redirect('blog:create_post')


@login_required
def add_comment(request, post_id):
    """Добавление комментария к посту."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        url = reverse('blog:post_detail', kwargs={'post_id': post.id})
        return redirect(f'{url}#comment_{comment.id}')
    comments = (
        Comment.objects.filter(post=post)
        .select_related('author')
        .order_by('created_at')
    )
    return render(request,
                  "blog/detail.html",
                  {'post': post, 'form': form, 'comments': comments})


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария."""
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)
    if request.user != comment.author:
        raise Http404
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post.id)
    return render(request, 'blog/comment.html', {'form': form,
                                                 'comment': comment,
                                                 'post': post})


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if request.user != comment.author:
        raise Http404

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post.id)

    return render(request, 'blog/comment.html', {'comment': comment,
                                                 'post': post})
