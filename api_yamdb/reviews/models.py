from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Выберите категорию'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        help_text='Выберите жанр'
    )
    slug = models.SlugField(max_length=20, unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        help_text='Выберите название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр',
        related_name='titles'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание')

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


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


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    score = models.IntegerField(
        blank=False,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
