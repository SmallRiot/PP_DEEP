from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import DocumentViewSet, CombineImagesToPDFView

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')


urlpatterns = [
    path('', include(router.urls)),
    path('api/combine_pdf', CombineImagesToPDFView.as_view(), name='combine_images_to_pdf'),
]