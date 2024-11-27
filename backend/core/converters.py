import io
import os
from PIL import Image
from django.core.files.base import ContentFile
from pdf2image import convert_from_bytes
from django.conf import settings
from PyPDF2 import PdfReader, PdfWriter


def remove_dir(session_id,
              base_folder):
    from core.models import Document, MedicalInsurance
    import shutil

    if os.path.exists(base_folder):
        for item in os.listdir(base_folder):
            item_path = os.path.join(base_folder, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

    try:
        shutil.rmtree(base_folder)
        print(f"Directory '{base_folder}' and its contents deleted successfully.")
    except OSError as e:
        print(f"Error: {e.strerror}")

    Document.objects.filter(session_id=session_id).delete()

    medicalInsurance = MedicalInsurance.objects.get(session_id=session_id)
    medicalInsurance.father.delete()
    medicalInsurance.mother.delete()
    medicalInsurance.delete()




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
        else:
            return self._process_image()


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
        from core.models import Document

        base_folder = os.path.join(settings.MEDIA_ROOT, 'backend/documents', session_id)
        output_pdf_path = os.path.join(base_folder, f'{session_id}_combined.pdf')

        if os.path.exists(output_pdf_path):
            return output_pdf_path  # Возвращаем существующий путь, если файл уже создан

        image_files = []

        pdf_files = []

        for root, dirs, files in os.walk(base_folder):
            for file in files:
                if file.endswith(".png"):
                    image_files.append(os.path.join(root, file))
                elif file.endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))


        image_files.sort()
        pdf_files.sort()

        # images = [Image.open(file).convert('RGB') for file in image_files]
        pdf_writer = PdfWriter()

        for image_file in image_files:
            image = Image.open(image_file).convert('RGB')
            image_pdf = io.BytesIO()
            image.save(image_pdf, format='PDF')
            image_pdf.seek(0)
            image_pdf_reader = PdfReader(image_pdf)
            for page_num in range(len(image_pdf_reader.pages)):
                pdf_writer.add_page(image_pdf_reader.pages[page_num])

        for pdf_file in pdf_files:
            with open(pdf_file, 'rb') as pdf:
                pdf_reader = PdfReader(pdf)
                pdf_writer.append_pages_from_reader(pdf_reader)

        with open(output_pdf_path, 'wb') as output_pdf_file:
            pdf_writer.write(output_pdf_file)

        # if images:
        #     from core.models import Document
        #     images[0].save(output_pdf_path, save_all=True, append_images=images[1:])


        Document.objects.create(
            name =f'{session_id}_combined.pdf',
            session_id=session_id,
            path=output_pdf_path.replace(settings.MEDIA_ROOT, '')  # Относительный путь для хранения
        )

        return output_pdf_path



