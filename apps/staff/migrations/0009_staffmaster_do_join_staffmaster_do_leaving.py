# Generated by Django 5.1 on 2024-09-27 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_staffattendance_submitted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffmaster',
            name='do_join',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staffmaster',
            name='do_leaving',
            field=models.DateField(blank=True, null=True),
        ),
    ]