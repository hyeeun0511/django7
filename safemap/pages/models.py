# 혜은==========================================1224
from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,      # :star: 추가
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
# 혜은==========================================1224