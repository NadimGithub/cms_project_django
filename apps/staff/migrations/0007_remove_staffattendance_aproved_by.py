# Generated by Django 5.1 on 2024-09-26 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_alter_staffattendance_aproved_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffattendance',
            name='aproved_by',
        ),
    ]
