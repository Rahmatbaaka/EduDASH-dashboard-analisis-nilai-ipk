# pbo/urls.py

from django.contrib import admin
from django.urls import path
from dashboard.views import dashboard_view  # Mengimpor fungsi dari views.py

urlpatterns = [
    path('admin/', admin.site.urls),
    # Baris di bawah ini yang akan memunculkan dashboard di halaman     utama (root URL)     
    path('', dashboard_view, name='dashboard'), 
]