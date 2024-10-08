# Generated by Django 5.1.1 on 2024-10-01 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_number', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('domain', models.CharField(max_length=255)),
                ('year_founded', models.CharField(max_length=255)),
                ('industry', models.CharField(max_length=255)),
                ('size_range', models.CharField(max_length=255)),
                ('locality', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('linkedin_url', models.URLField(max_length=255)),
                ('current_employee_estimate', models.CharField(max_length=255)),
                ('total_employee_estimate', models.CharField(max_length=255)),
            ],
        ),
    ]
