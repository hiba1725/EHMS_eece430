from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

class Patient(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient', primary_key=True)
	age = models.IntegerField(null=True, blank=True)
	phone_number = models.CharField(max_length=15, null=True, blank=True)
	address = models.CharField(max_length=100, null=True, blank=True)
	role = models.CharField(max_length=10, default='Patient')

	def __str__(self):
		return f"{self.user.username} {self.user.first_name} {self.user.last_name}"

class CreditCard(models.Model):
	card_num = models.CharField(max_length=20)
	cvv = models.CharField(max_length=3)
	name = models.CharField(max_length=60)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)


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
