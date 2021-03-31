from django.shortcuts import render

from .models import Appointment
from . import functions

def day_selector(request):
    """
    Day selector view

    """
    doctor = "Dr. Halawi"
    return render(request,"appointment/day_selector.html",{"doctor":doctor})

def slot_selector(request):
    """
    Slot selector view

    """
    day = request.POST["day"]
    doctor = request.POST["doctor_name"]
    Appointment.objects.filter(day=day,doctor=doctor)
    return render(request,"appointment/slot_selector.html")

def confirmation(request):
    """
    Confirmation view

    """
    pass



