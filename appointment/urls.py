from django.urls import path

from . import views

app_name = 'appointment'
urlpatterns = [
    path('day-selector', views.day_selector, name='day_select'),
    path('slot-selector/', views.slot_selector, name='slot_select'),
    path('confirm/', views.confirmation, name='confirmation')
]