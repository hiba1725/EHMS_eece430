from django.forms.utils import ErrorDict
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.decorators import login_required

from .models import Doctor
from .forms import DoctorForm, UserForm


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
    if request.user.is_authenticated and request.user.doctor.role == "Doctor":
            return render(request, 'doctor/dashboard.html')
    return redirect('/doctor/login')


def edit_account_info(request):
    if request.user.is_authenticated and request.user.patient.role == "Patient":
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
    return redirect('/doctor/login')


def edit_password(request):
    if request.user.is_authenticated and request.user.patient.role == "Patient":
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
    return redirect('/doctor/login')

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