from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class BlogPost(models.Model):
   title = models.CharField(max_length=200)
   content = models.TextField()
   author = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='blog_posts'
   )
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
      ordering = ['-created_at']

   def __str__(self):
      return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    # Used for nested replies
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username} - {self.post.title}'


class PostLike(models.Model):
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post_likes'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'],
                name='unique_post_like'
            )
        ]

    def __str__(self):
        return f'{self.user.username} liked {self.post.title}'


class CommentLike(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='comment_likes'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment_likes'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['comment', 'user'],
                name='unique_comment_like'
            )
        ]

    def __str__(self):
        return f'{self.user.username} liked comment {self.comment.id}'


class PostRating(models.Model):
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post_ratings'
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'],
                name='unique_post_rating'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.post.title} - {self.rating}/5'


   
