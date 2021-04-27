from django.forms.utils import ErrorDict
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from .forms import ManagerForm, UserForm
from .models import Manager, Report
from appointment.models import Appointment
from doctor.models import Doctor
from customer.models import Patient
from doctor.forms import DoctorForm
from customer.forms import PatientForm
from datetime import datetime

def login_manager(request):
	if request.user.is_authenticated:
		try:
			if request.user.manager.role == "Manager":
				return redirect('manager/get_report')
		except Exception as e:
			print(e)
			return render(request, 'manager/login.html',
						  {'error_message': 'Invalid Login. Make sure to be logged out.'})
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		try:
			if user.manager.role != "Manager":
				raise
		except Exception as e:
			print(e)
			return render(request, 'manager/login.html', {'error_message': 'Invalid Login'})
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('manager/get_report')
			else:
				return render(request, 'manager/login.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'manager/login.html', {'error_message': 'Invalid login'})
	return render(request, 'manager/login.html')


def logout_manager(request):
	if not request.user.is_authenticated:
		return redirect('/')
	try:
		logout(request)
		return redirect('/')
	except Exception as e:
		print(e)


def add_manager(request):
	if request.user.is_authenticated and request.user.manager.role == "Manager":
		if request.POST:
			user_form = UserForm(request.POST)
			print(user_form.is_bound)
			print(user_form.is_valid())
			if user_form.is_valid():
				user = user_form.save(commit=False)
				password = request.POST["password"]
				try:
					password_validation.validate_password(password)
				except Exception as e:
					errAsDict = {'password': ErrorDict({'': '\n'.join(e.messages)})}
					return render(request, 'manager/add_manager.html',
								  {'user_form_error': ErrorDict(errAsDict)})
				passwordConfirm = request.POST["passwordConfirm"]
				if password != passwordConfirm:
					return render(request, 'manager/add_manager.html',
								  {'password': ErrorDict({'': "Passwords do not match"})})
				user.set_password(password)
				user.save()
				manager = Manager()
				manager.user = user
				manager.role = "Manager"
				manager.save()
				login(request, user)
				return redirect('/manager/get_report')
			else:
				return render(request, 'manager/add_manager.html',
							  {'user_form_error': user_form.errors})
		return render(request, 'manager/add_manager.html')
	return redirect('/')


def add_doctor(request):
	if request.user.is_authenticated and request.user.manager.role == "Manager":
		if request.POST:
			user_form = UserForm(request.POST)
			doctor_form = DoctorForm(request.POST)
			if user_form.is_valid() and doctor_form.is_valid():
				if int(request.POST["age"]) <= int(request.POST["years_of_experience"]):
					return render(request, 'manager/add_doctor.html', {'other_errors': ErrorDict({"Years of Experience": ErrorDict({'': "Years of experience cannot be equal or greater than age"})})})
				user = user_form.save(commit=False)
				password = request.POST["password"]
				try:
					password_validation.validate_password(password)
				except Exception as e:
					errAsDict = {'password': ErrorDict({'': '\n'.join(e.messages)})}
					return render(request, 'manager/add_doctor.html',
								  {'user_form_error': ErrorDict(errAsDict)})
				passwordConfirm = request.POST["passwordConfirm"]
				if password != passwordConfirm:
					return render(request, 'manager/add_doctor.html', {'other_errors': ErrorDict({"Password": ErrorDict({'': "Passwords do not match"})})})
				user.set_password(password)
				user.save()
				doctor = doctor_form.save(commit=False)
				doctor.user = user
				doctor.role = "Doctor"
				doctor.save()
				return redirect('/manager/get_report')
			else:
				return render(request, 'manager/add_doctor.html',
							  {'user_form_error': user_form.errors, 'doctor_form_error': doctor_form.errors})
		else:
			return render(request, 'manager/add_doctor.html')
	return redirect('/')


def add_patient(request):
	if request.user.is_authenticated and request.user.manager.role == "Manager":
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
					return render(request, 'manager/add_patient.html',
								  {'user_form_error': ErrorDict(errAsDict)})
				passwordConfirm = request.POST["passwordConfirm"]
				if password != passwordConfirm:
					return render(request, 'manager/add_patient.html', {'other_errors': ErrorDict({"Password": ErrorDict({'': "Passwords do not match"})})})
				user.set_password(password)
				user.save()
				patient = patient_form.save(commit=False)
				patient.user = user
				patient.role = "Patient"
				patient.save()
				return redirect('/manager/get_report')
			else:
				return render(request, 'manager/add_patient.html',
							  {'user_form_error': user_form.errors, 'patient_form_error': patient_form.errors})
		else:
			return render(request, 'manager/add_patient.html')
	return redirect('/')


def edit_doctor(request, doctor_pk):
	if request.user.is_authenticated and request.user.manager.role == "Manager":
		doctor_info = Doctor.objects.get(pk=doctor_pk)
		if request.POST:
			user_form = UserForm(request.POST, instance=doctor_info.user)
			doctor_form = DoctorForm(request.POST, instance=doctor_info)
			if user_form.is_valid() and doctor_form.is_valid():
				username = request.POST['username']
				password = request.POST['password']
				user = authenticate(username=username, password=password)
				if user is not None:
					if int(request.POST["age"]) <= int(request.POST["years_of_experience"]):
						return render(request, 'manager/edit_doctor.html', {'other_errors': ErrorDict({"Years of Experience": ErrorDict({'': "Years of experience cannot be equal or greater than age"})})})
					user = user_form.save(commit=False)
					user.set_password(request.POST["password"])
					user.save()
					doctor = doctor_form.save(commit=False)
					doctor.user = user
					doctor.save()
					return redirect('/manager/get_report')
				else:
					return render(request, 'manager/edit_doctor.html',
								{'user_form_error': user_form.errors,
								'doctor_form_error': doctor_form.errors,
								'other_errors': ErrorDict({"Password": ErrorDict({'': "Wrong Password"})}),
								'doctor': doctor_info})
			else:
				return render(request, 'manager/edit_doctor.html',
								{'user_form_error': user_form.errors,
								'doctor_form_error': doctor_form.errors,
								'doctor': doctor_info})
		return render(request, 'manager/edit_doctor.html', {'doctor': doctor_info})
	return redirect('/')


def edit_patient(request, patient_pk):
	if request.user.is_authenticated and request.user.manager.role == "Manager":
		patient_info = Patient.objects.get(pk=patient_pk)
		if request.POST:
			user_form = UserForm(request.POST, instance=patient_info.user)
			patient_form = PatientForm(request.POST, instance=patient_info)
			if user_form.is_valid() and patient_form.is_valid():
				username = request.POST['username']
				password = request.POST['password']
				user = authenticate(username=username, password=password)
				if user is not None:
					user = user_form.save(commit=False)
					user.set_password(request.POST["password"])
					user.save()
					patient = patient_form.save(commit=False)
					patient.user = user
					patient.save()
					return redirect('/manager/get_report')
				else:
					return render(request, 'manager/edit_patient.html',
								{'user_form_error': user_form.errors,
								'patient_form_error': patient_form.errors,
								'other_errors': ErrorDict({"Password": ErrorDict({'': "Wrong Password"})}),
								'patient': patient_info})
			else:
				return render(request, 'manager/edit_patient.html',
								{'user_form_error': user_form.errors, 'patient_form_error': patient_form.errors, 'patient': patient_info})
		return render(request, 'manager/edit_patient.html', {'patient': patient_info})
	return redirect('/')


def delete_doctor(request, doctor_pk):
	if request.user.is_authenticated and request.user.manager.role == "Manager":
		doctor = Doctor.objects.get(pk=doctor_pk)
		doctor.user.delete()
		return redirect('/manager/doctors')
	return redirect('/')


def delete_patient(request, patient_pk):
	if request.user.is_authenticated and request.user.manager.role == "Manager":
		patient = Patient.objects.get(pk=patient_pk)
		patient.user.delete()
		return redirect('/manager/patients')
	return redirect('/')


def delete_appointment(request, appointment_pk):
	if request.user.is_authenticated and request.user.manager.role == "Manager":
		appointment = Appointment.objects.get(pk=appointment_pk)
		appointment.delete()
		return redirect('/manager/appointments')
	return redirect('/')


def get_report(request):
	if request.user.is_authenticated and request.user.manager.role == "Manager":
		patients = Patient.objects.filter(role="Patient").exclude(user__username="admin")
		doctors = Doctor.objects.filter(role="Doctor").exclude(user__username="admin")
		appointments = Appointment.objects.all()
		num_patients = len(patients)
		num_doctors = len(doctors)
		num_appointments_month = 0
		month = datetime.today().month
		for appointment in appointments:
			if appointment.date.month == month:
				num_appointments_month += 1
		return render(request, 'manager/report.html',
					  {'num_patients': num_patients,
					   'num_doctors': num_doctors,
					   'num_appointments_month': num_appointments_month
					   })
	return redirect('/')


def doctors(request):
	if request.user.is_authenticated and request.user.manager.role == "Manager":
		doctors = Doctor.objects.filter(role="Doctor").exclude(user__username="admin")
		for doctor in doctors:
			num_appointment = len(Appointment.objects.filter(doctor=doctor))
			doctor.num_appointment = num_appointment
		return render(request, 'manager/doctors.html', {'doctors': doctors})
	return redirect('/')


def patients(request):
	if request.user.is_authenticated and request.user.manager.role == "Manager":
		patients = Patient.objects.filter(role="Patient").exclude(user__username="admin")
		for patient in patients:
			num_appointment = len(Appointment.objects.filter(patient=patient))
			patient.num_appointment = num_appointment
		return render(request, 'manager/patients.html', {'patients': patients})
	return redirect('/')


def appointments(request):
	if request.user.is_authenticated and request.user.manager.role == "Manager":
		appointments = Appointment.objects.all()
		return render(request, 'manager/appointments.html', {'appointments': appointments})
	return redirect('/')
