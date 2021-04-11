from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'doctor'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_account_info/', views.edit_account_info, name='edit_account_info'),
    path('edit_password/', views.edit_password, name='edit_password'),
    path('search_doctors/', views.search_doctors, name="dsearch"),
    path('search_patient/', views.search_patient, name="search_patient"),
]