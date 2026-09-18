from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count,Avg

from .models import BlogPost,Comment,CommentLike
from .forms import PostForm,CommentForm


def home(request):
    posts = BlogPost.objects.select_related( 'author').prefetch_related(
        'comments',
        'likes',
        'ratings'
    )

    return render(request,'blog_post/home.html',{'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(
        BlogPost.objects
        .select_related('author')
        .prefetch_related(
            'comments',
            'likes',
            'ratings'
        )
        .annotate(
            total_comments=Count(
                'comments',
                distinct=True
            ),
            total_likes=Count(
                'likes',
                distinct=True
            ),
            total_ratings=Count(
                'ratings',
                distinct=True
            ),
            average_rating=Avg(
                'ratings__rating'
            ),
        ),
        id=id
    )

    comments = (
        post.comments
        .filter(parent__isnull=True)
        .select_related('author')
        .prefetch_related(
            'replies__author'
        )
    )

    return render(
        request,
        'blog_post/post_details.html',
        {
            'post': post,
            'comments': comments
        }
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

@login_required
def add_comment(request, id):
    post = get_object_or_404(BlogPost, id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect('post_detail', id=post.id)

    else:
        form = CommentForm()

    return render(
        request,
        'blog_post/comment_form.html',
        {
            'form': form,
            'post': post,
            'title': 'Add Comment'
        }
    )

@login_required
def edit_comment(request, id):
    comment = get_object_or_404(
        Comment,
        id=id,
        author=request.user
    )

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()

            return redirect(
                'post_detail',
                id=comment.post.id
            )

    else:
        form = CommentForm(instance=comment)

    return render(
        request,
        'blog_post/comment_form.html',
        {
            'form': form,
            'post': comment.post,
            'comment': comment,
            'title': 'Edit Comment'
        }
    )

@login_required
def delete_comment(request, id):
    comment = get_object_or_404(
        Comment,
        id=id,
        author=request.user
    )

    post_id = comment.post.id

    if request.method == 'POST':
        comment.delete()

    return redirect(
        'post_detail',
        id=post_id
    )

@login_required
def add_reply(request, id):
    parent_comment = get_object_or_404(
        Comment,
        id=id
    )

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = parent_comment.post
            reply.author = request.user
            reply.parent = parent_comment
            reply.save()

            return redirect(
                'post_detail',
                id=parent_comment.post.id
            )

    else:
        form = CommentForm()

    return render(
        request,
        'blog_post/comment_form.html',
        {
            'form': form,
            'post': parent_comment.post,
            'parent_comment': parent_comment,
            'title': 'Reply to Comment'
        }
    )