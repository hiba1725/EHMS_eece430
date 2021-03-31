from django.shortcuts import render

from .models import Appointment
from doctor.models import Doctor
from . import functions

def day_selector(request,doctor_name):
    """
    Day selector view

    """
    return render(request,"appointment/day_selector.html",{"doctor":doctor_name})

def slot_selector(request,doctor_name):
    """
    Slot selector view

    """
    day = request.GET["day"]
    doctor = Doctor.objects.get(name=doctor_name)
    appts = Appointment.objects.filter(date=day,doctor_id=doctor)
    slots = functions.find_available_slots(appts)
    return render(request,"appointment/slot_selector.html",{"available_slots":slots})

def confirmation(request):
    """
    Confirmation view

    """
    pass



