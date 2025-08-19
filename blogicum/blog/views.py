from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .constants import POSTS_ON_MAIN
from .models import Category, Post
from .utils import get_base_post


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
