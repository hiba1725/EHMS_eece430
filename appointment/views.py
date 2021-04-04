from django.shortcuts import render, redirect

from .models import Appointment
from doctor.models import Doctor
from customer.models import Patient
from . import functions

def day_selector(request,doctor_name):
    """
    Day selector view

    """
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        return render(request,"appointment/day_selector.html",{"doctor":doctor_name})
    return redirect('/customer/login')

def slot_selector(request,doctor_name):
    """
    Slot selector view

    """
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        day = request.GET["day"]
        doctor = Doctor.objects.get(name=doctor_name)
        appts = Appointment.objects.filter(date=day,doctor_id=doctor)
        slots = functions.find_available_slots(appts)
        return render(request,"appointment/slot_selector.html",{"doctor":doctor_name,"available_slots":slots,"day":day})
    return redirect('/customer/login')

def confirmation(request,doctor_name,day):
    """
    Confirmation view

    """
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        slot = request.GET["select-slot"]
        return render(request,"appointment/confirmation.html",{"doctor":doctor_name,"slot":slot,"day":day})
    return redirect('/customer/login')

def book(request,doctor_name,day,slot):
    """
    Book appointment view

    """
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        doctor = Doctor.objects.get(name=doctor_name)
        patient = request.user.patient
        slot_encoded = functions.encode_slot(slot)
        appt = Appointment(doctor=doctor,patient=patient,date=day,slot=slot_encoded)
        appt.save()
        return render(request,"appointment/booked.html")
    return redirect('/customer/login')



