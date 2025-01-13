# Generated by Django 5.1.4 on 2024-12-26 15:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skillpoint_api', '0009_alter_department_organisation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='skillpoint_api.user'),
        ),
    ]