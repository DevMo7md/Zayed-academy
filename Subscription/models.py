from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=30)
        super().save(*args, **kwargs)

    def is_active(self):
        return self.end_date >= datetime.now()

    def __str__(self):
        return f"{self.user.username}'s subscription"
