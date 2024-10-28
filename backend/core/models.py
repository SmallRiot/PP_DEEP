import os

from django.db import models

# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=100)
    session_id = models.CharField(max_length=100, blank=True, null=True)  # Поле для сессии
    path = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            name, ext = os.path.splitext(self.path.name)
            self.name = name
        super().save(*args, **kwargs)