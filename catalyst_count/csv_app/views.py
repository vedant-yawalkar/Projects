from django.shortcuts import render
from django.http import JsonResponse
from .forms import CSVUploadForm, QueryForm
from .models import CSVData
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            handle_uploaded_file(fs.path(filename))
            return JsonResponse({'status': 'success'})
    else:
        form = CSVUploadForm()
    return render(request, 'csv_app/upload.html', {'form': form})

def handle_uploaded_file(file_path):
    chunksize = 1000
    existing_names = set(CSVData.objects.values_list('name', flat=True))  # Collect existing names in a set
    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        for index, row in chunk.iterrows():
            name = str(row.get('Name', '')).strip() if pd.notna(row.get('Name')) else ''
            # Check if name already exists, if so, skip adding the record
            if name in existing_names:
                continue

            domain = str(row.get('Domain', '')).strip() if pd.notna(row.get('Domain')) else ''
            year_founded = row.get('Year Founded')
            industry = str(row.get('Industry', '')).strip() if pd.notna(row.get('Industry')) else ''
            employees = row.get('Employees')
            location = str(row.get('Location', '')).strip() if pd.notna(row.get('Location')) else ''
            linkedin_url = str(row.get('Linkedin url', '')).strip() if pd.notna(row.get('Linkedin url')) else ''
            current_employees = row.get('Current Employees')

            year_founded = int(year_founded) if pd.notna(year_founded) else 0
            employees = int(employees) if pd.notna(employees) else 0
            current_employees = int(current_employees) if pd.notna(current_employees) else 0

            # Check if all numeric fields are 0, if so, skip adding the record
            if year_founded == 0 and employees == 0 and current_employees == 0:
                continue

            CSVData.objects.create(
                name=name,
                domain=domain,
                year_founded=year_founded,
                industry=industry,
                employees=employees,
                location=location,
                linkedin_url=linkedin_url,
                current_employees=current_employees,
            )
            existing_names.add(name)  # Add new name to the existing names set


def query_data(request):
    data = CSVData.objects.all()
    return render(request, 'csv_app/query.html', {'data': data})

def query_count(request):
    form = QueryForm(request.GET)
    data = []
    count = 0
    if form.is_valid():
        filters = {}
        if form.cleaned_data['name']:
            filters['name__icontains'] = form.cleaned_data['name']
        if form.cleaned_data['domain']:
            filters['domain__icontains'] = form.cleaned_data['domain']
        if form.cleaned_data['year_founded'] is not None:
            filters['year_founded'] = form.cleaned_data['year_founded']
        if form.cleaned_data['industry']:
            filters['industry__icontains'] = form.cleaned_data['industry']
        if form.cleaned_data['employees'] is not None:
            filters['employees'] = form.cleaned_data['employees']
        if form.cleaned_data['location']:
            filters['location__icontains'] = form.cleaned_data['location']
        if form.cleaned_data['linkedin_url']:
            filters['linkedin_url__icontains'] = form.cleaned_data['linkedin_url']
        if form.cleaned_data['current_employees'] is not None:
            filters['current_employees'] = form.cleaned_data['current_employees']

        data = CSVData.objects.filter(**filters)
        count = data.count()

    return render(request, 'csv_app/query_data.html', {'form': form, 'count': count, 'data': data})

@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and conform password are not same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')