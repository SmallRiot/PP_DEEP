import io
import os
from PIL import Image
from django.core.files.base import ContentFile
from pdf2image import convert_from_bytes
from django.conf import settings



class FileConverter:
    """Класс для конвертации файлов в нужный формат."""

    def __init__(self, file=None, name=None):
        self.file = file
        self.name = name
        if self.file:
            self.file_ext = os.path.splitext(self.file.name)[1].lower()
        else:
            self.file_ext = None

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

    def convert_images_to_pdf(self, session_id):
        # Получаем путь к папке с изображениями
        base_folder = os.path.join(settings.MEDIA_ROOT, 'documents', session_id)

        # Находим все .png файлы в папке session_id, включая вложенные
        image_files = []
        for root, dirs, files in os.walk(base_folder):
            for file in files:
                if file.endswith(".png"):
                    image_files.append(os.path.join(root, file))

        # Сортируем файлы по пути, чтобы страницы были в нужном порядке
        image_files.sort()

        # Открываем изображения и конвертируем в формат, пригодный для PDF
        images = [Image.open(file).convert('RGB') for file in image_files]

        # Создаем результирующий PDF
        if images:
            from core.models import Document
            output_pdf_path = os.path.join(base_folder, f'{session_id}_combined.pdf')
            images[0].save(output_pdf_path, save_all=True, append_images=images[1:])

            # Сохраняем информацию о новом PDF в базе данных, создавая новую запись
            Document.objects.create(
                session_id=session_id,
                path=output_pdf_path.replace(settings.MEDIA_ROOT, '')  # Относительный путь для хранения
            )

        return output_pdf_path