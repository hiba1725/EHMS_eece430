from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    path('', include('pages.urls')),
    path('customer/', include('customer.urls'), name='customer'),
    path('doctor/', include('doctor.urls'), name='doctor'),
    path('appointment/', include('appointment.urls'), name='appointment'),
    path('manager', include('manager.urls'), name='manager'),
    url(r'^', include('django_private_chat.urls')),
    url(r'',include('chat.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)