from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('traffic', '교통사고'),
    ('violence', '폭력/위협'),
    ('fire', '화재/연기'),
    ('lost', '분실/도난'),
    ('etc', '기타'),
]

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=120)
    content = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()
    happened_at = models.DateTimeField()
    summary = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='etc')
    risk = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
