from django.contrib import admin

from .models import Patient, CreditCard

admin.site.register(Patient)
admin.site.register(CreditCard)