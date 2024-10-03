# views.py
import csv
import io
from concurrent.futures import ThreadPoolExecutor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import UploadedFile, CompanyInfo
from .serializers import FileUploadSerializer, CompanyInfoSerializer

# Create a global ThreadPoolExecutor for managing threads
executor = ThreadPoolExecutor(max_workers=5)
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

                # Use threading to handle the CSV processing asynchronously
                def process_csv():
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
            
            # Submit the task to ThreadPoolExecutor
            executor.submit(process_csv)
            
            return Response({"status": "success", "file_id": uploaded_file.id}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class QueryBuilderView(APIView):
    def get(self,request, *args, **kwargs):
        distinct_industries = CompanyInfo.objects.values('industry').distinct()
        distinct_years_founded = CompanyInfo.objects.values('year_founded').distinct()

        distinct_localities = CompanyInfo.objects.values('locality').distinct()
        distinct_cities = []
        distinct_states = []
        for locality in distinct_localities:
            locality_parts = locality['locality'].split(', ')
            if len(locality_parts) >= 2:
                distinct_cities.append(locality_parts[0])
                distinct_states.append(locality_parts[1])

        distinct_countries = CompanyInfo.objects.values('country').distinct()
        distinct_employees_from = CompanyInfo.objects.values('current_employee_estimate').distinct()
        distinct_employees_to = CompanyInfo.objects.values('total_employee_estimate').distinct()

        return render(request, 'query_builder.html', {
            'distinct_industries': distinct_industries,
            'distinct_years_founded': distinct_years_founded,
            'distinct_cities': distinct_cities,
            'distinct_states': distinct_states,
            'distinct_countries': distinct_countries,
            'distinct_employees_from': distinct_employees_from,
            'distinct_employees_to': distinct_employees_to,
        })

    def post(self,request, *args, **kwargs):
        keyword = request.data.get('keyword')
        industry = request.data.get('industry')
        year_founded = request.data.get('year_founded')
        city = request.data.get('city')
        state = request.data.get('state')
        country = request.data.get('country')
        employees_from = request.data.get('employeesFrom')
        employees_to = request.data.get('employeesTo')
        
        filtered_data = CompanyInfo.objects.all()
        
        if keyword:
            filtered_data = filtered_data.filter(name__icontains=keyword)
        
        if industry:
            filtered_data = filtered_data.filter(industry=industry)
        
        if year_founded:
            filtered_data = filtered_data.filter(year_founded=year_founded)
        
        if city:
            filtered_data = filtered_data.filter(locality__icontains=city)
        
        if state:
            filtered_data = filtered_data.filter(locality__icontains=state)
        
        if country:
            filtered_data = filtered_data.filter(country=country)
        
        if employees_from:
            filtered_data = filtered_data.filter(current_employee_estimate__gte=employees_from)
        
        if employees_to:
            filtered_data = filtered_data.filter(total_employee_estimate__lte=employees_to)
        
        filtered_count = filtered_data.count()
        
        serializer = CompanyInfoSerializer(filtered_data, many=True)

        return Response({'filtered_count': filtered_count, 'filtered_data': serializer.data}, status=status.HTTP_200_OK)