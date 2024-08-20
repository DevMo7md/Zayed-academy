from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
import pytz

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)  # جعلها يمكن أن تكون null أو blank

    def save(self, *args, **kwargs):
        # تعيين تواريخ الاشتراك إذا لم تكن موجودة
        if self.end_date is None:
            if self.start_date is None:
                self.start_date = datetime.now(pytz.timezone('Africa/Cairo'))  # تعيين تاريخ البدء مع منطقة زمنية
            self.end_date = self.start_date + timedelta(days=30)  # تعيين فترة الاشتراك كـ 30 يوماً من تاريخ البدء
        super().save(*args, **kwargs)

    def is_active(self):
        # التأكد من أن end_date موجودة وأنه يتم مقارنة كائنات datetime مع معلومات حول المناطق الزمنية
        return self.end_date and self.end_date >= datetime.now(pytz.timezone('Africa/Cairo'))

    def __str__(self):
        return f"{self.user.username}'s subscription"
