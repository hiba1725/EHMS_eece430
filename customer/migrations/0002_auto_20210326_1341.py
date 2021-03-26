# Generated by Django 3.1.6 on 2021-03-26 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='cardInfo',
        ),
        migrations.AddField(
            model_name='creditcard',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.patient'),
        ),
    ]
