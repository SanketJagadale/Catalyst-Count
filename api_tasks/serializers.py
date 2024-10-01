from rest_framework import serializers
from .models import UploadedFile

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file']

    def validate_file(self, value):
        # Check if the uploaded file is a CSV
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("File is not a CSV.")
        return value
