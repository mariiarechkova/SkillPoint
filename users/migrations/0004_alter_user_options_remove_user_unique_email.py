# Generated by Django 5.1.5 on 2025-02-12 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_role_weight_vote_alter_user_weight_vote'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveConstraint(
            model_name='user',
            name='unique_email',
        ),
    ]
