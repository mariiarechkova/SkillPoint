# Generated by Django 5.1.3 on 2024-12-16 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skillpoint_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='start_work_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
