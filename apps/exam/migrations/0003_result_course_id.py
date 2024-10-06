# Generated by Django 5.1 on 2024-09-30 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_coursemaster_submitted_by_and_more'),
        ('exam', '0002_remove_result_subject_id_result_division_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='course_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.coursemaster'),
        ),
    ]
