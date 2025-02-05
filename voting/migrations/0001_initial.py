# Generated by Django 5.1.5 on 2025-02-05 19:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.CharField(choices=[('week', 'Week'), ('month', 'Month'), ('quarter', 'Quarter'), ('year', 'Year')], default='month', max_length=10)),
                ('start_day', models.IntegerField(blank=True, default=1)),
                ('end_day', models.IntegerField(blank=True, default=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.organisation')),
            ],
        ),
        migrations.CreateModel(
            name='VoteDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estimation', models.FloatField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('judge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='judge', to=settings.AUTH_USER_MODEL)),
                ('rated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated_user', to=settings.AUTH_USER_MODEL)),
                ('vote_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote_event', to='voting.voteevent')),
            ],
        ),
    ]
