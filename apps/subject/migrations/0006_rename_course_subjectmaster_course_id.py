# Generated by Django 5.1 on 2024-09-30 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0005_remove_subjectmaster_course_id_subjectmaster_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subjectmaster',
            old_name='course',
            new_name='course_id',
        ),
    ]