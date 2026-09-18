from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import BlogPost
from .forms import PostForm


def home(request):
    posts = BlogPost.objects.all()

    return render(request,'blog_post/home.html',{'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)

    return render(
        request,
        'blog_post/post_details.html',
        {'post': post}
    )


@login_required
def create_post(request):

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(
                request,
                'Your post has been created successfully.'
            )

            return redirect('post_detail', id=post.id)

    else:
        form = PostForm()

    return render(
        request,
        'blog_post/create_post.html',
        {'form': form}
    )


@login_required
def edit_post(request, id):

    post = get_object_or_404(
        BlogPost,
        id=id,
        author=request.user
    )

    if request.method == 'POST':
        form = PostForm(
            request.POST,
            instance=post
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your post has been updated successfully.'
            )

            return redirect('post_detail', id=post.id)

    else:
        form = PostForm(instance=post)

    return render(
        request,
        'blog_post/edit_post.html',
        {
            'form': form,
            'post': post
        }
    )


@login_required
def delete_post(request, id):

    post = get_object_or_404(
        BlogPost,
        id=id,
        author=request.user
    )

    if request.method == 'POST':
        post.delete()

        messages.success(
            request,
            'Your post has been deleted successfully.'
        )

        return redirect('my_posts')

    return render(
        request,
        'blog_post/delete_post.html',
        {'post': post}
    )


@login_required
def my_posts(request):

    posts = BlogPost.objects.filter(
        author=request.user
    )

    return render(
        request,
        'blog_post/my_posts.html',
        {'posts': posts}
    )