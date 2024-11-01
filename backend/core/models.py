import os
from django.db import models
import pillow_heif

from core.utils import FileConverter

pillow_heif.register_heif_opener()


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

        ispdf = False
        final_path = f'documents/{self.session_id or "default_session"}/'
        if self.path.name.endswith('.pdf'):
            ispdf = True
            final_path += self.name

        if self.path:
            if self.path.name.endswith('.png'):
                final_filename = f"{self.name}.png"
                self.path.name = os.path.join(final_path, final_filename)
            elif self.path.name.endswith('combined.pdf'):
                self.path.name = os.path.join(final_path, self.path.name)
            else:
                converter = FileConverter(self.path, self.name)
                converted_files = converter.process_file()

                self.path.delete(save=False)

                for file_content, filename in converted_files:
                    file_path = os.path.join(final_path, filename)
                    self.path.save(file_path, file_content, save=False)

                if ispdf:
                    self.path.name = final_path

        super().save(*args, **kwargs)
