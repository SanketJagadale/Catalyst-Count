import os
from rest_framework import serializers
from .models import UploadedFile, CompanyInfo

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file']

    def validate_file(self, value):
        # Check if the uploaded file is a CSV
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("File is not a CSV.")

        # Check if a file with the same name already exists
        uploaded_file_name = os.path.basename(value.name)
        if UploadedFile.objects.filter(file__endswith=uploaded_file_name).exists():
            raise serializers.ValidationError("A file with this name already exists.")
        return value

class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = '__all__'
