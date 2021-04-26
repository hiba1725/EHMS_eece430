from django.urls import path, re_path

from . import views

app_name = 'manager'
urlpatterns = [
	re_path(r'^/?$', views.login_manager, name='login_manager'),
	re_path(r'^/logout/?$', views.logout_manager, name="logout_manager"),
	re_path(r'^/add_manager/?$', views.add_manager, name='add_manager'),
	re_path(r'^/add_doctor/?$', views.add_doctor, name='add_doctor'),
	re_path(r'^/add_patient/?$', views.add_patient, name='add_patient'),
	re_path(r'^/edit_doctor/(?P<doctor_pk>\w+)/?$', views.edit_doctor, name='edit_doctor'),
	re_path(r'^/edit_patient/(?P<patient_pk>\w+)/?$', views.edit_patient, name='edit_patient'),
	re_path(r'^/delete_doctor/(?P<doctor_pk>\w+)/?$', views.delete_doctor, name='delete_doctor'),
	re_path(r'^/delete_patient/(?P<patient_pk>\w+)/?$', views.delete_patient, name='delete_patient'),
	re_path(r'^/delete_appointment/(?P<appointment_pk>\w+)/?$', views.delete_appointment, name='delete_appointment'),
	re_path(r'^/get_report/?$', views.get_report, name='get_report'),
	re_path(r'^/doctors/?$', views.doctors, name='doctors'),
	re_path(r'^/patients/?$', views.patients, name='patients'),
	re_path(r'^/appointments/?$', views.appointments, name='appointments'),
]