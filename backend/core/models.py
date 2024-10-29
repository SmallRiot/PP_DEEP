import os
from django.db import models
import pillow_heif

from core.utils import FileConverter

pillow_heif.register_heif_opener()


# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=100)
    session_id = models.CharField(max_length=100, blank=True, null=True)  # Поле для сессии
    path = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            name, ext = os.path.splitext(self.path.name)
            self.name = name

        final_path = f'documents/{self.session_id or "default_session"}/'
        if self.path.name.endswith('.pdf'):
            final_path += self.name

        if self.path:
            file_ext = os.path.splitext(self.path.name)[1].lower()
            if file_ext == '.png':
                # Сохраняем PNG по новому пути
                final_filename = f"{self.name}.png"
                self.path.name = os.path.join(final_path, final_filename)
            else:
                # Используем FileConverter для конвертации файлов
                converter = FileConverter(self.path, self.name)
                new_content, final_filename = converter.convert_to_png()

                # Удаляем временный файл после обработки
                self.path.delete(save=False)
                final_full_path = os.path.join(final_path, final_filename)
                self.path.save(final_full_path, new_content, save=False)


        super().save(*args, **kwargs)
