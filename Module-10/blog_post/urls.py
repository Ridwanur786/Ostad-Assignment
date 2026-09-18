from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'post/<int:id>/',
        views.post_detail,
        name='post_detail'
    ),

    path(
        'post/create/',
        views.create_post,
        name='create_post'
    ),

    path(
        'post/<int:id>/edit/',
        views.edit_post,
        name='edit_post'
    ),

    path(
        'post/<int:id>/delete/',
        views.delete_post,
        name='delete_post'
    ),

    path(
        'my-posts/',
        views.my_posts,
        name='my_posts'
    ),

  # Comments
    path(
        'post/<int:id>/comment/add/',
        views.add_comment,
        name='add_comment'
    ),

    path(
        'comment/<int:id>/edit/',
        views.edit_comment,
        name='edit_comment'
    ),

    path(
        'comment/<int:id>/delete/',
        views.delete_comment,
        name='delete_comment'
    ),

    # Replies
    path(
        'comment/<int:id>/reply/',
        views.add_reply,
        name='add_reply'
    ),
]