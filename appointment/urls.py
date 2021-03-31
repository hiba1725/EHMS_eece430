from django.urls import path

from . import views

app_name = 'appointment'
urlpatterns = [
    path('<str:doctor_name>/day', views.day_selector, name='day_select'),
    path('<str:doctor_name>/slot', views.slot_selector, name='slot_select'),
    path('<str:doctor_name>/confirm', views.confirmation, name='confirmation')
]