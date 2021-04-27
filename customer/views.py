from django.forms.utils import ErrorDict
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Patient, CreditCard
from .forms import PatientForm, UserForm, CardForm
from appointment.models import Appointment


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.POST:
        user_form = UserForm(request.POST)
        patient_form = PatientForm(request.POST)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            password = request.POST["password"]
            try:
                password_validation.validate_password(password)
            except Exception as e:
                errAsDict = {'password': ErrorDict({'': '\n'.join(e.messages)})}
                return render(request, 'customer/signup.html',
                              {'user_form_error': ErrorDict(errAsDict)})
            passwordConfirm = request.POST["passwordConfirm"]
            if password != passwordConfirm:
                return render(request, 'customer/signup.html', {'other_errors': ErrorDict({"Password": ErrorDict({'': "Passwords do not match"})})})
            if not all(x.isdigit() for x in request.POST["phone_number"]):
                return render(request, 'customer/signup.html', {'other_errors': ErrorDict({"Phone Number": ErrorDict({'': "Phone number should be made of digits only"})})})
            user.set_password(password)
            user.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.role = "Patient"
            patient.save()
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'customer/signup.html',
                          {'user_form_error': user_form.errors, 'patient_form_error': patient_form.errors})
    else:
        return render(request, 'customer/signup.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.patient.role != "Patient":
                raise
        except Exception as e:
            print(e)
            return render(request, 'customer/login.html', {'error_message': 'Invalid Login'})
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'customer/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'customer/login.html', {'error_message': 'Invalid login'})
    return render(request, 'customer/login.html')


def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('/')
    try:
        logout(request)
        return redirect('/')
    except Exception as e:
        print(e)


def account_info(request):
    if request.user.is_authenticated and request.user.patient.role == "Patient":
            appointments = Appointment.objects.filter(patient=request.user.patient)
            return render(request, 'customer/account_info.html')
    return redirect('/customer/login')


def appointments(request):
    if request.user.is_authenticated and request.user.patient.role == "Patient":
            appointments = Appointment.objects.filter(patient=request.user.patient)
            return render(request, 'customer/appointments.html', {'appointments':appointments})
    return redirect('/customer/login')


def payments(request):
    if request.user.is_authenticated and request.user.patient.role == "Patient":
            appointments = Appointment.objects.filter(patient=request.user.patient)
            return render(request, 'customer/payment_methods.html')
    return redirect('/customer/login')


def add_card(request):
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        if request.POST:
            card_form = CardForm(request.POST)
            if card_form.is_valid():
                card = card_form.save(commit=False)
                card.patient = request.user.patient
                card.save()
                return redirect('/customer/account')
            else:
                return render(request, 'customer/add_card.html', {'card_form_error': card_form.errors})
        return render(request, 'customer/add_card.html')
    return redirect('/customer/login')


def remove_card(request):
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        cards = CreditCard.objects.filter(patient_id=request.user.id)
        if request.POST:
            id = request.POST["choice"]
            card = CreditCard.objects.filter(patient=request.user.patient)
            # card = get_object_or_404(CreditCard, pk=id)
            card.delete()
            cards = CreditCard.objects.filter(patient_id=request.user.id)
        return render(request, 'customer/remove_card.html', {'cards': cards})
    return redirect('/customer/login')


def edit_account_info(request):
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        if request.POST:
            user_form = UserForm(request.POST, instance=request.user, )
            patient_form = PatientForm(request.POST, instance=request.user.patient)
            if user_form.is_valid() and patient_form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if not all(x.isdigit() for x in request.POST["phone_number"]):
                        return render(request, 'customer/edit_account_info.html', {'other_errors': ErrorDict({"Phone Number": ErrorDict({'': "Phone number should be made of digits only"})})})
                    user = user_form.save(commit=False)
                    user.set_password(request.POST["password"])
                    user.save()
                    patient = patient_form.save(commit=False)
                    patient.user = user
                    patient.save()
                    login(request, user)
                else:
                    return render(request, 'customer/edit_account_info.html',
                                  {'user_form_error': user_form.errors,
                                   'patient_form_error': patient_form.errors,
                                   'other_errors': ErrorDict({"Password": ErrorDict({'': "Wrong Password"})})})
                return redirect('/customer/account/')
            else:
                return render(request, 'customer/edit_account_info.html',
                              {'user_form_error': user_form.errors, 'patient_form_error': patient_form.errors})
        return render(request, 'customer/edit_account_info.html')
    return redirect('/customer/login')


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
                    errAsDict = {'password': ErrorDict({'': '\n'.join(e.messages)})}
                    return render(request, 'customer/edit_password.html', {'errors': ErrorDict(errAsDict)})
                passwordnew2 = request.POST["passwordnew2"]
                if passwordnew1 != passwordnew2:
                    return render(request, 'customer/edit_password.html', {'errors': ErrorDict({"Password": ErrorDict({'': "Passwords do not match"})})})
                user.set_password(passwordnew1)
                user.save()
                login(request, user)
                return redirect('/customer/account')
            else:
                return render(request, 'customer/edit_password.html', {'errors': ErrorDict({"Password": ErrorDict({'': "Old password is incorrect"})})})
        return render(request, 'customer/edit_password.html')
    return redirect('/customer/login')


def view_history(request):
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        query = Appointment.objects.filter(patient = request.user.pk).order_by('-date')
        history = []
        for q in query:
            appts = {}
            appts['name'] = q.doctor.user.username
            appts['date'] = q.date
            appts['problem'] = q.problem
            appts['analysis'] = q.analysis
            appts['medication'] = q.medications
            history.append(appts)
        return render(request, 'customer/history.html', {'history': history})
    return redirect('/customer/login/')


def delete_patient(request):
    if request.user.is_authenticated and request.user.patient.role == "Patient":
        user = User.objects.filter(pk=request.user.pk)
        user.delete()
        return redirect('/')
    return redirect('/')