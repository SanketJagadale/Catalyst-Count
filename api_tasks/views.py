# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import UploadedFile
from .serializers import FileUploadSerializer

class FileUploadView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'upload.html')  # Render the HTML template

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.save()
            return Response({"status": "success", "file_id": uploaded_file.id}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

