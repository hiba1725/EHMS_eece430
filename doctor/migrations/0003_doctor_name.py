# Generated by Django 3.1.7 on 2021-03-31 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_auto_20210330_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='name',
            field=models.CharField(default='', max_length=20),
        ),
    ]
