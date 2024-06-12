from django.contrib import admin
from .models import CSVData

@admin.register(CSVData)
class CSVDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'year_founded', 'industry', 'employees', 'location', 'linkedin_url', 'current_employees')
    search_fields = ('name', 'domain', 'industry', 'location')

# Alternatively, if you prefer the simpler registration:
# admin.site.register(CSVData, CSVDataAdmin)
