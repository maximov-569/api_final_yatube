from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

MAX_LENGTH_TITLE: int = 200
MAX_LENGTH_SLUG: int = 15


class Group(models.Model):
    """Uses for creating groups of posts with same theme."""

    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        verbose_name='Название группы',
        help_text='Введите название группы',
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='url группы',
        help_text='Придумайте url группы',
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Введите описание группы',
    )

    def __str__(self):
        """Redefine __str__ method."""
        # Return title of group.
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    """Follow model.
    Provide opportunity to users to follow favorite authors.
    user and author FK that makes connection between follower and author.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='can_follow_once'
            ),
        ]
