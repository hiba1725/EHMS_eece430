from django.db import models

from doctor.models import Doctor
from customer.models import Patient

class Appointment(models.Model):
    """
    Appointment model

    Attributes 
    doctor_id, patient_id, date, slot

    """
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    date = models.DateField()
    slot = models.IntegerField()
    done = models.BooleanField(default=False)
    problem = models.CharField(max_length = 20000,default = 'none')
    analysis = models.CharField(max_length = 20000,default = 'none')
    medications = models.CharField(max_length = 20000,default = 'none')
