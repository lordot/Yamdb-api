from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


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
