from django.urls import path
from .views import upload_file, query_data, query_count
from csv_app import views

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('query/', query_data, name='query'),
    path('query_count/', query_count, name='query_count'),
]
