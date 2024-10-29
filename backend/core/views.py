from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from core.models import Document
from core.serializers import DocumentSerializer


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

        # Устанавливаем session_id
        session_id = request.session.session_key
        request.session['session_id'] = session_id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Передаем session_id в perform_create
        self.perform_create(serializer, session_id)
        headers = self.get_success_headers(serializer.data)

        # Устанавливаем session_id
        #serializer.instance.session_id = request.session.session_key
        #serializer.instance.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, session_id=None):
        serializer.save(session_id=session_id)