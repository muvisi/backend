# Generated by Django 4.1.2 on 2022-10-18 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_roomsbooking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomsbooking',
            name='user',
        ),
    ]
