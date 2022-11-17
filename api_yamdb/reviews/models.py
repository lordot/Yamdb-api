from django.core.validators import MinValueValidator, MaxValueValidator
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

    class Meta:
        verbose_name_plural = "Пользователи"


class Review(models.Model):
    # заглушка user
    author = models.IntegerField()
    # заглушка title
    title = models.IntegerField()
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    score = models.IntegerField(
        blank=False,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
