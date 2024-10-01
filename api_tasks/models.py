from django.db import models

# Create your models here.

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class CompanyInfo(models.Model):
    company_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    year_founded = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    size_range = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    linkedin_url = models.URLField(max_length=255)
    current_employee_estimate = models.CharField(max_length=255)
    total_employee_estimate = models.CharField(max_length=255)

    def __str__(self):
        return self.name
