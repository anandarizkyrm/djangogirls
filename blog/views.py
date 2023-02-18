from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from blog.form import CategoryForm, PostForm
from .models import Category, Post
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model
from datetime import time

User = get_user_model()


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')

    total_post = Post.objects.aggregate(total_post=Count('id'))

    context = {
        "posts": posts,
        "total_posts": total_post,
    }
    return render(request, 'blog/post_list.html', context)


def create_post(request):

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('detail_post', id=post.id)
    else:
        form = PostForm()
    context = {"form": form}
    return render(request, 'blog/create_post.html', context)

def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else: 
        form = CategoryForm()
    return render(request, 'blog/create_category.html', {"form": form})        

def get_post_by_category(request, category_id):
    posts = Post.objects.filter(categories=category_id)
    context = {
        "posts" : posts
    }

    return render(request, 'blog/category_list.html', context)

def categories(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, 'blog/category_list.html', context)


def detail_post(request, id):
    detail_post = get_object_or_404(Post, id=id)
    print(detail_post)
    context = {"detail": detail_post}

    return render(request, 'blog/detail_post.html', context)


def edit_post(request, id):

    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('detail_post', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {"form": form})
