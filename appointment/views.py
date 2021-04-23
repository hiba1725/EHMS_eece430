from django.shortcuts import render, redirect

from datetime import datetime

from .models import Appointment
from doctor.models import Doctor
from customer.models import Patient
from . import functions

def day_selector(request,doctor_pk):
    """
    Day selector view

    """
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        # doctors = Doctor.objects.all()
        # for doc in doctors:
        #     print(doc.pk, doc.user.first_name)
        doctor = Doctor.objects.get(pk=doctor_pk)
        return render(request,"appointment/day_selector.html",{"doctor":doctor,"error":""})
    return redirect('/customer/login/')

def slot_selector(request,doctor_pk):
    """
    Slot selector view

    """
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        doctor = Doctor.objects.get(pk=doctor_pk)
        day = request.GET["day"]
        print(day)
        day_datetime = datetime.strptime(day,"%Y-%m-%d")
        today = datetime.today()
        if(day_datetime < today):
            # apptment in past
            return render(request,"appointment/day_selector.html",{"doctor":doctor,"error":"You cannot book an appointment in the past"})
        elif(day_datetime.weekday() == 6):
            # sunday
            return render(request,"appointment/day_selector.html",{"doctor":doctor,"error":"You cannot book an appointment on a Sunday"})
        else:
            appts = Appointment.objects.filter(date=day,doctor_id=doctor)
            slots = functions.find_available_slots(appts)
            return render(request,"appointment/slot_selector.html",{"doctor":doctor,"available_slots":slots,"day":day})
    return redirect('/customer/login/')

def confirmation(request,doctor_pk,day):
    """
    Confirmation view

    """
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        slot = request.GET["select-slot"]
        doctor = Doctor.objects.get(pk=doctor_pk)
        return render(request,"appointment/confirmation.html",{"doctor":doctor,"slot":slot,"day":day})
    return redirect('/customer/login/')

def book(request,doctor_pk,day,slot):
    """
    Book appointment view

    """
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        doctor = Doctor.objects.get(pk=doctor_pk)
        patient = request.user.patient
        slot_encoded = functions.encode_slot(slot)
        appt = Appointment(doctor=doctor,patient=patient,date=day,slot=slot_encoded)
        appt.save()
        return render(request,"appointment/booked.html")
    return redirect('/customer/login/')
