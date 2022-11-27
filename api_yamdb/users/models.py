from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

    email = models.EmailField(
        'email address',
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

    class Meta:
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_user(self):
        return self.role == 'user'
