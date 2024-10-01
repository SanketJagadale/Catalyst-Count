# views.py
import csv
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import UploadedFile, CompanyInfo
from .serializers import FileUploadSerializer, CompanyInfoSerializer

class FileUploadView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'upload.html')  # Render the HTML template

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.save()

            #import only companies_sorted csv file into Database table(CompanyInfo)
            if uploaded_file.file == 'uploads/companies_sorted.csv':
                csv_file = uploaded_file.file  
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                reader = csv.reader(io_string)
                next(reader)

                companies_sorted_list = []

                for row in reader:
                    company_number, name, domain, year_founded, industry, size_range, \
                    locality, country, linkedin_url, current_employee_estimate, \
                    total_employee_estimate = row
                    data = CompanyInfo(
                        company_number=company_number,
                        name=name,
                        domain=domain,
                        year_founded=year_founded,
                        industry=industry,
                        size_range=size_range,
                        locality=locality,
                        country=country,
                        linkedin_url=linkedin_url,
                        current_employee_estimate=current_employee_estimate,
                        total_employee_estimate=total_employee_estimate
                    )
                    companies_sorted_list.append(data)

                # Bulk create products in the database
                CompanyInfo.objects.bulk_create(companies_sorted_list)  

            return Response({"status": "success", "file_id": uploaded_file.id}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

