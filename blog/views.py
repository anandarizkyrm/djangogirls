from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import is_valid_path
from django.utils import timezone
from django.shortcuts import redirect
from blog.form import CategoryForm, FilterPostForm, PostForm, CommentForm, AuthForm, RegisterForm, UserProfileForm
from .models import Category, Comment, Post
from django.db.models import Sum, Count
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib import messages

User = get_user_model()


def editprofile(request, id):
    user = get_object_or_404(User, id=id)
    form = UserProfileForm(request.POST or None, instance=user)
    if request.user.id != id:
        return HttpResponse("Cannot Edit User you Are not this user",
                            status=401)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.info(request, 'Success update your profile')
            return redirect('editprofile', id)

    return render(request, 'blog/editprofile.html', {
        'form': form,
        'user': user
    })


def userprofile(request, id):
    user = get_object_or_404(User, id=id)
    posts = Post.objects.filter(author=user).order_by('-created_date')
    total_post = Post.objects.filter(author=user).aggregate(
        total_post=Count('id'))

    context = {
        'posts': posts,
        'total_post': total_post['total_post'],
        'user': user
    }

    return render(request, 'blog/profile.html', context)


def signin(request):
    type: str = request.GET.get('type')

    print(type)

    if type == "register":
        form = RegisterForm(request.POST or None)
    else:
        form = AuthForm(request, request.POST or None)

    if request.method == 'POST':

        if form.is_valid() and type != 'register':
            return redirect('post_list')
        elif form.is_valid() and type == 'register':
            form.save()
            messages.info(request, 'Success register Please Login')
            return redirect('signin')

    return render(request, 'blog/signin.html', {'form': form, 'type': type})


# Create your views here.
def post_list(request):
    # posts = Post.objects.filter(
    #     published_date__lte=timezone.now()).order_by('published_date')

    posts = Post.objects.all().order_by('-created_date')
    total_post = Post.objects.aggregate(total_post=Count('id'))

    blog_posts = Post.objects.values(
        'title', 'id', 'visits', 'created_date', 'author_id',
        'author__username', 'author__last_name').order_by('-created_date')[:5]

    print(blog_posts)

    if request.method == 'POST':
        form = FilterPostForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            categories = form.cleaned_data['categories']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            if search and categories:
                posts = Post.objects.filter(
                    Q(title__icontains=search)
                    | Q(categories__in=categories)).order_by('-created_date')
            elif search:
                posts = Post.objects.filter(
                    Q(title__icontains=search)).order_by('-created_date')
            elif categories:
                posts = Post.objects.filter(
                    Q(categories__in=categories)).order_by('-created_date')
            elif date_from and date_to:
                posts = Post.objects.filter(
                    created_date__gte=date_from,
                    created_date__lte=date_to).order_by('-created_date')
    else:
        form = FilterPostForm(request.POST)

    posts_paginator = Paginator(posts, 1)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = posts_paginator.get_page(page_number)

    context = {
        "posts": page_obj.object_list,
        "page_obj": page_obj,
        "total_posts": total_post,
        "form": form,
    }
    return render(request, 'blog/post_list.html', context)


def create_post(request):

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            post = form.save(commit=False)
            post.author = request.user
            # post.categories = request.POST('categories')
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('detail_post', id=post.id)
        elif not request.user.is_authenticated:
            return HttpResponse('You are not authenticated, Please log in')
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


def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST' and request.user == post.author:
        post.delete()
        return redirect('post_list')
    else:
        return HttpResponse(status=401)


def get_post_by_category(request, category_id):
    posts = Post.objects.filter(categories=category_id)
    context = {"posts": posts}

    return render(request, 'blog/category_list.html', context)


def categories(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, 'blog/category_list.html', context)


def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    else:
        return HttpResponse(status=405)


def detail_post(request, id):
    detail_post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = id
            comment.save()
            return redirect('detail_post', id=id)
    else:
        form = CommentForm()

    context = {"detail": detail_post, "form": form}

    return render(request, 'blog/detail_post.html', context)


def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)

    if request.method == 'POST':
        comment.delete()
        return redirect('detail_post', id=comment.post_id)


def edit_post(request, id):

    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('detail_post', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {"form": form})
