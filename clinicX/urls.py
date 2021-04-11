from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('pages.urls')),
    path('customer/', include('customer.urls'), name='customer'),
    path('doctor/', include('doctor.urls'), name='doctor'),
    path('appointment/', include('appointment.urls'), name='appointment'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)