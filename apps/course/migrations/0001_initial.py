# Generated by Django 5.1 on 2024-10-07 10:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institute', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('status', models.CharField(default='active', max_length=20)),
                ('intake_capacity', models.IntegerField()),
                ('durstion', models.CharField(blank=True, max_length=20, null=True)),
                ('institute_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institute.institutemaster')),
                ('submitted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DivisionMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('year', models.CharField(choices=[('1st year', '1st year'), ('2nd year', '2nd year'), ('Direct second year', 'Direct second year'), ('3rd year', '3rd year'), ('4th year', '4th year')], max_length=20)),
                ('semester', models.CharField(choices=[('1 semester', '1 semester'), ('2 semester', '2 semester'), ('3 semester', '3 semester'), ('4 semester', '4 semester'), ('5 semester', '5 semester'), ('6 semester', '6 semester'), ('7 semester', '7 semester'), ('8 semester', '8 semester')], max_length=20)),
                ('status', models.CharField(default='active', max_length=20)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.coursemaster')),
                ('submitted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
