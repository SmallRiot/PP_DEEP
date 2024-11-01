import os

from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Document
from core.serializers import DocumentSerializer
from core.utils import FileConverter


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
        headers = self.get_success_headers(serializer.data)



        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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