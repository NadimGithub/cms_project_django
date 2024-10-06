# Generated by Django 5.1 on 2024-09-30 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_coursemaster_submitted_by_and_more'),
        ('student', '0005_alter_studentdetails_dob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentmaster',
            name='course',
        ),
        migrations.RemoveField(
            model_name='studentmaster',
            name='division',
        ),
        migrations.RemoveField(
            model_name='studentmaster',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='studentmaster',
            name='year',
        ),
        migrations.AddField(
            model_name='studentdetails',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.coursemaster'),
        ),
        migrations.AddField(
            model_name='studentdetails',
            name='division',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='studentdetails',
            name='semester',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='studentdetails',
            name='year',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]