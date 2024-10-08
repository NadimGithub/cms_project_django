# Generated by Django 5.1 on 2024-10-07 11:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        ('institute', '0001_initial'),
        ('staff', '0001_initial'),
        ('subject', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10)),
                ('profile_image', models.ImageField(upload_to='student_profiles/')),
                ('role', models.CharField(default='student', max_length=30)),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institute.institutemaster')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentLeave',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'pending'), ('Approved', 'Approved'), ('rejected', 'rejected')], default='pending', max_length=10)),
                ('reason', models.TextField()),
                ('student_approved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_approved_leaves', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.studentmaster')),
            ],
        ),
        migrations.CreateModel(
            name='StudentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(blank=True, max_length=50, null=True)),
                ('semester', models.CharField(blank=True, max_length=50, null=True)),
                ('division', models.CharField(blank=True, max_length=50, null=True)),
                ('registration_number', models.CharField(max_length=20, unique=True)),
                ('blood_group', models.CharField(max_length=10)),
                ('category', models.CharField(choices=[('general', 'general'), ('obc', 'obc'), ('sc', 'sc'), ('st', 'st')], max_length=10)),
                ('caste', models.CharField(max_length=50)),
                ('education_qualification', models.CharField(max_length=50)),
                ('mother_name', models.CharField(max_length=50)),
                ('dob', models.DateField(blank=True, null=True)),
                ('nationality', models.CharField(choices=[('indian', 'Indian'), ('other', 'Other')], max_length=10)),
                ('admission_type', models.CharField(choices=[('cap', 'CAP'), ('management', 'Management')], max_length=10)),
                ('cap_id', models.CharField(max_length=20, unique=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.coursemaster')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='student.studentmaster')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.CharField(blank=True, max_length=50, null=True)),
                ('semester', models.CharField(blank=True, max_length=50, null=True)),
                ('division', models.CharField(blank=True, max_length=50, null=True)),
                ('date', models.DateField()),
                ('present', models.BooleanField(default=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.coursemaster')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staffmaster')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subject.subjectmaster')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.studentmaster')),
            ],
        ),
        migrations.CreateModel(
            name='PermAddress',
            fields=[
                ('permaddress_id', models.AutoField(primary_key=True, serialize=False)),
                ('perm_state', models.CharField(max_length=50)),
                ('perm_district', models.CharField(max_length=50)),
                ('perm_taluka', models.CharField(max_length=50)),
                ('perm_city', models.CharField(max_length=50)),
                ('perm_pincode', models.CharField(max_length=6)),
                ('perm_address', models.CharField(max_length=50)),
                ('staff_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='staff.staffmaster')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.studentmaster')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('document_id', models.AutoField(primary_key=True, serialize=False)),
                ('document_name', models.CharField(max_length=50)),
                ('document', models.FileField(upload_to='')),
                ('document_uploded', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('staff_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='staff.staffmaster')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.studentmaster')),
            ],
        ),
        migrations.CreateModel(
            name='StudentProgress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_id', models.CharField(max_length=10)),
                ('marks', models.FloatField()),
                ('grade', models.CharField(max_length=2)),
                ('attendance', models.FloatField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.studentmaster')),
            ],
        ),
        migrations.CreateModel(
            name='TempAddress',
            fields=[
                ('tempaddress_id', models.AutoField(primary_key=True, serialize=False)),
                ('temp_state', models.CharField(max_length=50)),
                ('temp_district', models.CharField(max_length=50)),
                ('temp_taluka', models.CharField(max_length=50)),
                ('temp_city', models.CharField(max_length=50)),
                ('temp_pincode', models.CharField(max_length=6)),
                ('temp_address', models.CharField(max_length=50)),
                ('staff_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='staff.staffmaster')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.studentmaster')),
            ],
        ),
    ]
