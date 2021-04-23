from .models import Appointment
from datetime import datetime, timedelta
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from clinicX.settings import EMAIL_HOST


def email_doctor(name, time, patient, email):
    try:
        send_mail(f"Appointment Reminder",
                  f"Dear Dr. {name}, you have an appointment at {time} with {patient}. Do not forget to prepare for it.",
                  EMAIL_HOST, [email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return HttpResponseRedirect('/')


def email_patient(name, time, doctor, email):
    try:
        send_mail(f"Appointment Reminder",
                  f"Dear valued customer {name}, you have an appointment at {time}:00 with {doctor}.",
                  EMAIL_HOST, [email])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return HttpResponseRedirect('/')


def appointments_email():
    today = datetime.today()
    hour = today.hour
    slot = hour-8
    results = Appointment.objects.filter(date=today)
    for appointment in results:
        if appointment.slot-slot == 1:
            doc_email = appointment.doctor.user.email
            pat_email = appointment.patient.user.email
            doc_name = appointment.doctor.user.first_name + " " + appointment.doctor.user.last_name
            pat_name = appointment.patient.user.first_name + " " + appointment.patient.user.last_name
            time = 8+appointment.slot
            email_doctor(doc_name, time, pat_name, doc_email)
            email_patient(pat_name, time, doc_name, pat_email)
    print("Reminders run every 30 minutes")