from django.forms.utils import ErrorDict
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from .models import Doctor
from .forms import DoctorForm, UserForm
from appointment.models import Appointment
from datetime import datetime

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.POST:
        user_form = UserForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            password = request.POST["password"]
            try:
                password_validation.validate_password(password)
            except Exception as e:
                errAsDict = {'password': ErrorDict({'': '\n'.join(e.messages)})}
                return render(request, 'doctor/signup.html',
                              {'user_form_error': ErrorDict(errAsDict)})
            passwordConfirm = request.POST["passwordConfirm"]
            if password != passwordConfirm:
                return render(request, 'doctor/signup.html', {'password': ErrorDict({'': "Passwords do not match"})})
            user.set_password(password)
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.role = "Doctor"
            doctor.save()
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'doctor/signup.html',
                          {'user_form_error': user_form.errors, 'patient_form_error': doctor_form.errors})
    else:
        return render(request, 'doctor/signup.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.doctor.role != "Doctor":
                raise
        except Exception as e:
            print(e)
            return render(request, 'doctor/login.html', {'error_message': 'Invalid Login'})
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'doctor/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'doctor/login.html', {'error_message': 'Invalid login'})
    return render(request, 'doctor/login.html')


def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('/')
    try:
        logout(request)
        return redirect('/')
    except Exception as e:
        print(e)


def dashboard(request):
    if request.user.is_authenticated:
        try:
            if request.user.doctor.role != "Doctor":
                return redirect('/doctor/login/')
        except Exception as e:
            print(e)
            return redirect('/doctor/login/')
        doc = request.user.doctor
        form_hidden = DoctorForm(instance=doc)
        if request.method == "POST":
            form = DoctorForm(request.POST, request.FILES, instance=doc)
            if form.is_valid():
                form.save()
            else:
                err = form.errors
                print(err)
        appointments = Appointment.objects.filter(doctor=request.user.doctor).order_by('-date')
        todo_app = 0
        done_app = 0
        today = datetime.today()
        week_number = today.isocalendar()[1]
        week_appointment ={}
        for app in appointments:
            iso = app.date.isocalendar()
            if app.date.year == today.year and iso[1] == week_number+(today.isocalendar()[2]//7): # if sunday, we want next week
                week_appointment[iso[2]] = [app.slot, f"{app.patient.user.first_name} {app.patient.user.last_name}"]
            if app.done:
                done_app += 1
            else:
                todo_app += 1
        return render(request, 'doctor/dashboard.html',
                      {'appointments': appointments,
                       'done_app': done_app,
                       'todo_app': todo_app,
                       'week_appointment': week_appointment,
                       'total_app': len(appointments),
                       'form_hidden': form_hidden
                       })
    return redirect('/doctor/login/')


def edit_account_info(request):
    if request.user.is_authenticated and request.user.doctor.role == "Doctor":
        if request.POST:
            user_form = UserForm(request.POST, instance=request.user, )
            doctor_form = DoctorForm(request.POST, instance=request.user.patient)
            if user_form.is_valid() and doctor_form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    user = user_form.save(commit=False)
                    user.set_password(request.POST["password"])
                    user.save()
                    doctor = doctor_form.save(commit=False)
                    doctor.user = user
                    doctor.save()
                    login(request, user)
                else:
                    return render(request, 'doctor/edit_account_info.html',
                                  {'user_form_error': user_form.errors,
                                   'patient_form_error': doctor_form.errors,
                                   'other_errors': "Wrong password"})
                return redirect('/doctor/account')
            else:
                return render(request, 'doctor/edit_account_info.html',
                              {'user_form_error': user_form.errors, 'patient_form_error': doctor_form.errors})
        return render(request, 'doctor/edit_account_info.html')
    return redirect('/doctor/login/')


def edit_password(request):
    if request.user.is_authenticated and request.user.doctor.role == "Doctor":
        if request.POST:
            oldpass = request.POST["passwordold"]
            user = request.user.username
            user = authenticate(username=user, password=oldpass)
            if user is not None:
                try:
                    passwordnew1 = request.POST["passwordnew1"]
                    password_validation.validate_password(passwordnew1)
                except Exception as e:
                    return render(request, 'doctor/edit_password.html', {'errors': e.messages})
                passwordnew2 = request.POST["passwordnew2"]
                if passwordnew1 != passwordnew2:
                    return render(request, 'doctor/edit_password.html', {'errors': 'Passwords do not match'})
                user.set_password(passwordnew1)
                user.save()
                login(request, user)
                return redirect('/doctor/account')
            else:
                return render(request, 'doctor/edit_password.html', {'errors': 'Old password is not correct'})
        return render(request, 'doctor/edit_password.html')
    return redirect('/doctor/login/')


def search_doctors(request):
    st = request.GET('query')
    doctors = Doctor.objects.filter(specialty__icontains=st).order_by('-years_of_experience')
    return render(request, 'doctor/search_doctors.html', {'doctors:', doctors})


class DoctorSearch(TemplateView):
    template_name = 'doctor/search_doctors.html'


class DoctorSearchResult(ListView):
    model = Doctor
    template_name = 'doctor/doctors_list.html'

    def get_queryset(self, *args, **kwargs):
        val = self.request.GET.get("q")
        if val:
            queryset = Doctor.objects.filter(specialty__icontains=val).order_by('-years_of_experience')
        else:
            queryset = Doctor.objects.none()
        queryset = queryset.values_list()
        return render(self.request, 'doctor/doctors_list.html', {'queryset':queryset})


def search_patient(request):
    if request.user.is_authenticated and request.user.doctor.role == "Doctor":
        if request.POST:
            pass
        return render(request, 'doctor/search_patient.html')
    return redirect('/doctor/login/')


def patient_profile(request):
    pass