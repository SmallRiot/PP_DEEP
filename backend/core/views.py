from django.http import HttpResponse
from rest_framework import viewsets
from .models import TestModel
from .serializers import TestModelSerializer

def index(request):
    return HttpResponse("Добро пожаловать")

class TestModelViewSet(viewsets.ModelViewSet):
    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer