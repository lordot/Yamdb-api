from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

    email = models.EmailField(
        ('email address'),
        max_length=254,
        blank=False,
        unique=True
    )
    first_name = models.CharField('first name', max_length=150, blank=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=33,
        help_text='Администратор, модератор или пользователь.'
        'По умолчанию `user`.',
        choices=ROLES,
        default='user'
    )
    is_moderator = models.BooleanField(
        'moderator',
        default=False,
        help_text='Designates whether'
                  'this user should be treated as moderator.'
    )

    class Meta:
        verbose_name_plural = "Пользователи"
