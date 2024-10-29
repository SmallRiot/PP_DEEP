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
        self.file_ext = os.path.splitext(self.file.name)[1].lower()

    def process_file(self):
        """Обрабатывает файл в зависимости от типа и возвращает список файлов для сохранения."""
        if self.file_ext == '.png':
            # Если уже PNG, возвращаем исходный файл
            return [(self.file, self.file.name)]
        elif self.file_ext == '.pdf':
            return self._process_pdf()
        else:
            return self._process_image()

    def _process_pdf(self):
        """Обработка PDF файла, конвертация всех страниц в PNG."""
        pdf_bytes = self.file.read()
        images = convert_from_bytes(pdf_bytes)
        png_pages = []

        for i, img in enumerate(images):
            img = img.convert("RGB")
            temp_img = io.BytesIO()
            img.save(temp_img, format="PNG")
            temp_img.seek(0)
            page_filename = f"{self.name}_page_{i + 1}.png"
            png_pages.append((ContentFile(temp_img.read()), page_filename))

        return png_pages


    def _process_image(self):
        """Обработка других изображений (не PNG). Конвертирует изображение в PNG."""
        img = Image.open(self.file)
        img = img.convert("RGB")
        temp_img = io.BytesIO()
        img.save(temp_img, format="PNG")
        temp_img.seek(0)
        filename = f"{self.name}.png"
        return [(ContentFile(temp_img.read()), filename)]