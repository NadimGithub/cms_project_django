# Generated by Django 5.1 on 2024-10-01 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0008_rename_student_result_std_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='marks',
            field=models.IntegerField(),
        ),
    ]