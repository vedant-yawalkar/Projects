from django import forms

class CSVUploadForm(forms.Form):
    file = forms.FileField()

class QueryForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    domain = forms.CharField(max_length=255, required=False)
    year_founded = forms.IntegerField(required=False)
    industry = forms.CharField(max_length=255, required=False)
    employees = forms.IntegerField(required=False)
    location = forms.CharField(max_length=255, required=False)
    linkedin_url = forms.CharField(max_length=255, required=False)
    current_employees = forms.IntegerField(required=False)
