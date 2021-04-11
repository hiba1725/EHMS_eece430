from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor', primary_key=True)
    years_of_experience = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=15, default='01111111')
    specialty = models.CharField(max_length=15, default='General')
    address = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=10, default='none')
    gender = models.CharField(max_length=1, default='O')
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} {self.user.first_name} {self.user.last_name}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Doctor.objects.create(user=instance)
        # Patient.objects.create(user=instance)
    instance.patient.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        # instance.patient.save()
        instance.doctor.save()
    except Exception as e:
        print(e)
