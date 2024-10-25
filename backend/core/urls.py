from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import DocumentViewSet

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')


urlpatterns = [
    path('api/', include(router.urls)),
]