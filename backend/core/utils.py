import io
import os

from PIL import Image
from django.core.files.base import ContentFile
from pdf2image import convert_from_bytes


class FileConverter:
    """Класс для конвертации файлов в нужный формат."""

    def __init__(self, file, name):
        self.file = file
        self.name = name

    def convert_to_png(self):
        """Конвертирует PDF или изображение в формат PNG и возвращает байтовые данные."""
        file_ext = os.path.splitext(self.file.name)[1].lower()

        if file_ext == '.pdf':
            # Чтение содержимого PDF как байтов и конвертация в изображение
            pdf_bytes = self.file.read()
            images = convert_from_bytes(pdf_bytes, first_page=0, last_page=1)
            img = images[0]  # Первая страница PDF
        else:
            # Если не PDF, просто открываем изображение
            img = Image.open(self.file)

        # Конвертируем изображение в RGB (для совместимости) и в формат PNG
        img = img.convert("RGB")
        temp_img = io.BytesIO()
        img.save(temp_img, format="PNG")
        temp_img.seek(0)

        return ContentFile(temp_img.read()), f"{self.name}.png"