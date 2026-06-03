# pbo/urls.py

from django.contrib import admin
from django.urls import path
from dashboard.views import dashboard_view, export_history, export_dataset
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='dashboard'), 
    path('export/<str:format_type>/', export_history, name='export_history'),
    path('export/<str:format_type>/', export_dataset, name='export_dataset'),
    path('migrate-data/', views.migrate_csv_to_sql, name='migrate_data'),

]
