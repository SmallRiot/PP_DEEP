from rest_framework import serializers
from core.models import Document
import logging

logger = logging.getLogger(__name__)

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['path']

    def validate_path(self, value):
        if not value.name.endswith('.pdf'):
            logger.warning("Attempt to upload a non-PDF file: %s", value.name)
            raise serializers.ValidationError("Only PDF files are allowed.")
        return value