from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .constants import POSTS_ON_MAIN, POSTS_PER_PAGE
from .models import Category, Post, Comment
from .utils import get_base_post, get_paginated_post
from .forms import PostForm, EditUserForm, CommentForm


def index(request):
    posts = get_base_post()[:POSTS_ON_MAIN]
    return render(request, "blog/index.html", {"post_list": posts})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.filter(
            id=post_id,
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
    )
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
            is_published=True
        )
    )
    post_list = get_base_post().filter(category=category)

    return render(
        request,
        "blog/category.html",
        {'category': category, 'post_list': post_list})


def profile(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    is_owner = request.user.is_authenticated and request.user == author
    if is_owner:
        qs = (Post.objects
              .filter(author=author)
              .select_related('author', 'category', 'location')
              .order_by('-pub_date'))
    else:
        qs = (get_base_post()
              .filter(author=author)
              .select_related('author', 'category', 'location'))
    page_obj = get_paginated_post(request, qs, POSTS_PER_PAGE)
    context = {
        'author': author,
        'post_list': page_obj,
        'is_owner': is_owner,
        'page_obj': page_obj,
        'profile': author,
    }
    return render(request, 'blog/profile.html', context)


def edit_profile(request):
    Form = EditUserForm()
    if request.method == 'POST':
        form = Form(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile')
    else:
        form = Form(instance=request.user)
    return render(request, 'blog/user.html', {'form': form})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form', form})


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail')
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile')
    return render(request, 'blog/create.html', {'post': post,
                                                'is_delete': True})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post.objects, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('blog:comment', post_id=post_id)
    return render(request, "blog/comment.html", {'post': post, 'form': form})


@login_required
def edit_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)
    if request.user != comment.author:
        return redirect('pages:404')
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment.html', {'form': form,
                                                 'comment': comment,
                                                 'post': post})


@login_required
def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if request.user != comment.author:
        return redirect('pages:404')

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post.id)

    return render(request, 'blog/comment.html', {'comment': comment,
                                                 'post': post})


def post_list(request):
    posts = Post.objects.all()
    for post in posts:
        post.comment_count = post.comments.count()
    return render(request, 'blog/comment.html', {'posts': posts})
