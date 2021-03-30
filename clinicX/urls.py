from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('customer/', include('customer.urls'), name='customer'),
    path('doctor/', include('doctor.urls'), name='doctor'),
    path('admin/', admin.site.urls),
]
