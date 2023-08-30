from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    """Класс пользователей."""
    username = models.CharField(
        max_length=settings.NAME_LENGHT,
        verbose_name='Имя пользователя',
        unique=True,
        blank=False,
        validators=[validate_username],
        help_text=(f'Напишите ваше имя пользователя длиной '
                   f'от {settings.MIN_USERNAME} '
                   f'до {settings.MAX_USERNAME} символов')
    )
    email = models.EmailField(
        max_length=settings.EMAIL_LENGHT,
        verbose_name='Электронная почта',
        unique=True,
        blank=False
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Подписчик')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='following',
                                  verbose_name='Подписаться')

    def __str__(self) -> str:
        return (f'{self.user}, {self.following.username}')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]
