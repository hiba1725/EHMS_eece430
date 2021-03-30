from django.db import models

from doctor.models import Doctor
from customer.models import Patient

# Create your models here.
class Appointment(models.Model):
    """
    Appointment model

    Attributes 
    doctor_id, patient_id, date, slot

    """
    doctor_id = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient,on_delete=models.CASCADE)
    date = models.DateField()
    slot = models.IntegerField()
