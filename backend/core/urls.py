from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestModelViewSet

router = DefaultRouter()
router.register(r'testmodels', TestModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]