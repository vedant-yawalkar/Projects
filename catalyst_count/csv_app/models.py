from django.db import models

class CSVData(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    year_founded = models.IntegerField()
    industry = models.CharField(max_length=255)
    employees = models.IntegerField()
    location = models.CharField(max_length=255)
    linkedin_url = models.CharField(max_length=255)
    current_employees = models.IntegerField()
