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

        base_folder = os.path.join(settings.MEDIA_ROOT, 'documents', session_id)
        output_pdf_path = os.path.join(base_folder, f'{session_id}_combined.pdf')

        if os.path.exists(output_pdf_path):
            return output_pdf_path  # Возвращаем существующий путь, если файл уже создан

        image_files = []
        for root, dirs, files in os.walk(base_folder):
            for file in files:
                if file.endswith(".png"):
                    image_files.append(os.path.join(root, file))

        image_files.sort()

        images = [Image.open(file).convert('RGB') for file in image_files]

        if images:
            from core.models import Document
            images[0].save(output_pdf_path, save_all=True, append_images=images[1:])

            self.clear_dir(session_id,image_files,
                  output_pdf_path,
                  base_folder)

            Document.objects.create(
                session_id=session_id,
                path=output_pdf_path.replace(settings.MEDIA_ROOT, '')  # Относительный путь для хранения
            )

        return output_pdf_path

    def clear_dir(self,session_id,
                  image_files,
                  output_pdf_path,
                  base_folder):
        from core.models import Document
        import shutil


        if os.path.exists(base_folder):
            for item in os.listdir(base_folder):
                item_path = os.path.join(base_folder, item)
                if item_path != output_pdf_path:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)

        Document.objects.filter(session_id=session_id).exclude(
            path=output_pdf_path.replace(settings.MEDIA_ROOT, '')
        ).delete()

