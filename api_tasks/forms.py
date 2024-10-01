from django import forms
from .models import UploadedFile

# Create your forms here.

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
