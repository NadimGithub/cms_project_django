# Generated by Django 5.1 on 2024-09-21 07:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('task', models.CharField(max_length=255)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=10)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=30)),
                ('deadline', models.DateField()),
                ('assigned_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.staffmaster')),
            ],
        ),
    ]