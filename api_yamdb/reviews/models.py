from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user_email')
        ]
