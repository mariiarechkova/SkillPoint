# Generated by Django 5.1.5 on 2025-02-12 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0002_organisation_stability_departmentweight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmentweight',
            name='weight_vote',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='stability',
            field=models.FloatField(blank=True, default=1.5),
        ),
    ]
