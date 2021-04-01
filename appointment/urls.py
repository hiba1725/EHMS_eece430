from django.urls import path

from . import views

app_name = 'appointment'
urlpatterns = [
    path('<str:doctor_name>/day', views.day_selector, name='day_select'),
    path('<str:doctor_name>/slot', views.slot_selector, name='slot_select'),
    path('<str:doctor_name>/<str:day>/confirm', views.confirmation, name='confirmation'),
    path('<str:doctor_name>/<str:day>/<str:slot>/book', views.book, name='book')
]