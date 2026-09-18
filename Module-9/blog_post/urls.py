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
]