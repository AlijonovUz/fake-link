import uuid

from django.db import models
from datetime import timedelta
from django.utils import timezone


class Data(models.Model):
    url = models.URLField()
    code = models.CharField(max_length=8, unique=True, blank=True)
    expire_days = models.PositiveIntegerField()
    expired_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())[:8]
        if not self.expired_at:
            self.expired_at = timezone.now() + timedelta(days=self.expire_days)
        return super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expired_at

    def __str__(self):
        return f"{self.url} (expires: {self.expired_at})"

    class Meta:
        verbose_name = "Ma'lumot "
        verbose_name_plural = "Ma'lumotlar"
