# Generated by Django 5.1 on 2024-09-21 07:44

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        ('institute', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('state', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('number', models.CharField(max_length=15)),
                ('email', models.TextField(unique=True)),
                ('status', models.CharField(default='active', max_length=20)),
                ('dob', models.DateField()),
                ('profile', models.ImageField(upload_to='profiles/')),
                ('blood_group', models.CharField(max_length=10)),
                ('category', models.CharField(max_length=50)),
                ('role', models.CharField(choices=[('principal', 'Principal'), ('vice_principal', 'Vice_Principal'), ('hod', 'Hod'), ('teacher', 'Teacher'), ('accountant', 'Accountant'), ('clark', 'Clark'), ('examinetor', 'Examinetor'), ('librarian', 'Librarian'), ('lab_assistant', 'Lab_Assistant')], max_length=30)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.coursemaster')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institute.institutemaster')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StaffLeave',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'pending'), ('Approved', 'Approved'), ('rejected', 'rejected')], default='pending', max_length=10)),
                ('reason', models.TextField()),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_leaves', to=settings.AUTH_USER_MODEL)),
                ('verified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verified_leaves', to=settings.AUTH_USER_MODEL)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staffmaster')),
            ],
        ),
        migrations.CreateModel(
            name='StaffAttendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField(default=django.utils.timezone.now, editable=False)),
                ('status', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Absent', max_length=10)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staffmaster')),
            ],
        ),
    ]