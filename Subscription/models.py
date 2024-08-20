from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.end_date is None:
            if self.start_date is None:
                self.start_date = datetime.now()  # تعيين تاريخ البدء إذا كان غير محدد
            self.end_date = self.start_date + timedelta(days=30)  # تعيين فترة الاشتراك كـ 30 يوماً من تاريخ البدء
        super().save(*args, **kwargs)

    def is_active(self):
        return self.end_date and self.end_date >= datetime.now()  # تحقق من أن end_date موجود

    def __str__(self):
        return f"{self.user.username}'s subscription"
