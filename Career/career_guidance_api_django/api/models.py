from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username

class APICallCounter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_counters")
    date = models.DateField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "date")

    def __str__(self):
        return f"{self.user.username} {self.date} -> {self.count}"
