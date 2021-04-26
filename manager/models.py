from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Report(models.Model):
	date = models.DateField()
	totalPatient = models.IntegerField()
	totalDoctors = models.IntegerField()
	totalAppointments = models.IntegerField()


class Manager(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager', primary_key=True)
	role = models.CharField(max_length=10, default='none', null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Manager.objects.create(user=instance)
	instance.patient.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	try:
		instance.patient.save()
	except Exception as e:
		print(e)
