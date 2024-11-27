import os

from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Document
from core.serializers import DocumentSerializer
from core.converters import FileConverter

from core.doc_services import DataInspector

from core.doc_services import delete_garbage_file


def index(request):
    if not request.session.session_key:
        request.session.create()
    return HttpResponse("Добро пожаловать")


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):

        if not request.session.session_key:
            request.session.create()

        session_id = request.session.session_key
        request.session['session_id'] = session_id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer, session_id)

        # Первое заявление
        statement1 = '''
        {
          "Название документа": "Заявление",
          "Дата": "2023-10-01",
          "Подпись": true,
          "ФИО заявителя": "Цветков Андрей Георгиевич",
          "ФИО ребенка": "Цветков Денис Андреевич",
          "Дата рождения ребенка": "2011-12-03"
        }
        '''

        # Второе заявление
        statement2 = '''
        {
          "Название документа": "Заявление",
          "Дата": "2024-08-20",
          "Подпись": false,
          "ФИО заявителя": "Петров Сергей Александрович",
          "ФИО ребенка": "Петрова Анна Сергеевна",
          "Дата рождения ребенка": "2024-08-20"
        }
        '''

        # Первое св. о браке
        marriage_certificate1 = '''
        {
          "Название документа": "СВИДЕТЕЛЬСТВО О ЗАКЛЮЧЕНИИ БРАКА",
          "ФИО мужа": "Цветков Андрей Георгиевич",
          "ФИО жены": "Цветкова Виктория Александровна"
        }
        '''
        # Первое св. о рождении
        birth_certificate1 = '''
        {
          "Название документа": "СВИДЕТЕЛЬСТВО О РОЖДЕНИИ",
          "ФИО ребенка": "Цветков Денис Андреевич",
          "ДР ребенка": "03/12/2011",
          "ФИО отца": "Цветков Андрей Георгиевич",
          "ФИО матери": "Цветкова Виктория Александровна"
        }
        '''

        # Второе св. о браке
        marriage_certificate2 = '''
        {
          "Название документа": "СВИДЕТЕЛЬСТВО О ЗАКЛЮЧЕНИИ БРАКАa",
          "ФИО мужа": "Белов Сергей Юрьевич",
          "ФИО жены": "Белова Александра Андреевна"
        }
        '''

        # второе св. о рождении
        birth_certificate2 = '''
        {
          "Название документа": "СВИДЕТЕЛЬСТВО О РОЖДЕНИИa",
          "ФИО ребенка": "Белова Марина Сергеевна",
          "ДР ребенка": "30/07/2015",
          "ФИО отца": "Белов Сергей Юрьевич",
          "ФИО матери": "Белова Александра Андреевна"
        }
        '''
        saved_instance = serializer.instance

        # rquid = str(uuid.uuid4())
        # auth_token = ''
        #
        # access_token = get_access_token(rquid, auth_token)
        #
        # img_path = saved_instance.path.name
        # img_id = load_img(access_token, img_path)
        # if("marriage_certificate" in saved_instance.name):
        #     receipt_info1 = get_marriage_info(access_token, img_id)
        #     print("1")
        # elif ("birth_certificate" in saved_instance.name):
        #     receipt_info2 = get_birth_info(access_token, img_id)
        #     print("1")

        headers = self.get_success_headers(serializer.data)

        if("marriage_certificate" in saved_instance.name):
            inspector = DataInspector(marriage_certificate1)
            response= inspector.check_marriage_certificate(session_id)
            if (response.status_code == 400):
                delete_garbage_file(saved_instance.id)
                return response
        elif ("statement" in saved_instance.name):
            inspector = DataInspector(statement2)
            response= inspector.check_statement(session_id)
            if(response.status_code == 400):
                delete_garbage_file(saved_instance.id)
                return response
        elif ("birth_certificate" in saved_instance.name):
            inspector = DataInspector(birth_certificate1)
            response= inspector.check_birth_certificate(session_id)
            if (response.status_code == 400):
                delete_garbage_file(saved_instance.id)
                return response


        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer, session_id=None):
        serializer.save(session_id=session_id)



class CombineImagesToPDFView(APIView):
    def get(self, request):

        try:
            converter = FileConverter()
            output_pdf_path = converter.convert_images_to_pdf(request.session.session_key)

            if not os.path.exists(output_pdf_path):
                return JsonResponse({'error': 'PDF file could not be created.'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            with open(output_pdf_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{request.session.session_key}_combined.pdf"'
                return response
        except Document.DoesNotExist:
            return JsonResponse({'error': 'Session ID not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)