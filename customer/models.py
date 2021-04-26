from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, User

from django.db.models.signals import post_save
from django.dispatch import receiver

class Patient(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient', primary_key=True)
	age = models.IntegerField(default=0, validators=[MinValueValidator(9), MaxValueValidator(150)])
	phone_number = models.CharField(max_length=15, default='01111111')
	address = models.CharField(max_length=100, null=True, blank=True)
	role = models.CharField(max_length=10, default='none')
	gender = models.CharField(max_length=1, default='O')

	def __str__(self):
		return f"{self.user.username} {self.user.first_name} {self.user.last_name}"

class CreditCard(models.Model):
	card_num = models.CharField(max_length=20)
	cvv = models.CharField(max_length=3)
	name = models.CharField(max_length=60)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)

class MedicalRecord(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
	num_appoinments = models.IntegerField(default=0)
	# allergies
	# treatments
	# chronic illnesses
	# past diagnosis

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Patient.objects.create(user=instance)
	instance.patient.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	try:
		instance.patient.save()
	except Exception as e:
		print(e)
