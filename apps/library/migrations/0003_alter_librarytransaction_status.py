# Generated by Django 5.1 on 2024-10-03 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_librarytransaction_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarytransaction',
            name='status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]