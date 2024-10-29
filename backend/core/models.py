import io
import os
from django.core.files.base import ContentFile
from PIL import Image
from django.db import models
from pdf2image import convert_from_path, convert_from_bytes
import pillow_heif
pillow_heif.register_heif_opener()

from django.core.files.storage import default_storage
# Функция для генерации пути с использованием session_id
def get_upload_to(instance, filename):
    session_path = f'documents/{instance.session_id}/'

    if filename.endswith('.pdf'):
        return os.path.join(session_path, filename)

    return session_path

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

        if self.path.name.endswith('.pdf'):
            final_path = f'documents/{self.session_id or "default_session"}/{self.name}'
        else:
            final_path = f'documents/{self.session_id or "default_session"}/'

        # Проверяем, что файл загружен и не является PNG
        if self.path:
            file_ext = os.path.splitext(self.path.name)[1].lower()

            if file_ext == '.png':
                # Сохраняем PNG по новому пути
                final_filename = f"{self.name}.png"
                self.path.name = os.path.join(final_path, final_filename)

            else:
                # Проверка, если файл PDF
                if file_ext == '.pdf':
                    # Чтение содержимого PDF как байтов и конвертация в изображение
                    pdf_bytes = self.path.read()
                    images = convert_from_bytes(pdf_bytes, first_page=0, last_page=1)
                    img = images[0]  # Первая страница PDF
                else:
                    # Если не PDF, просто открываем изображение
                    img = Image.open(self.path)

                # Конвертируем изображение в RGB (для совместимости) и в формат PNG
                img = img.convert("RGB")
                temp_img = io.BytesIO()
                img.save(temp_img, format="PNG")
                temp_img.seek(0)

                # Удаляем временный файл после обработки
                self.path.delete(save=False)

                final_filename = f"{self.name}.png"

                # Сохраняем файл в окончательное место
                final_full_path = os.path.join(final_path, final_filename)
                self.path.save(final_full_path, ContentFile(temp_img.read()), save=False)


        super().save(*args, **kwargs)
