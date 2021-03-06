# Generated by Django 1.11.1 on 2019-06-19 12:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True)),
                ('status', models.CharField(choices=[('N', 'new'), ('P', 'in progress'), ('C', 'completed'), ('A', 'archived')], default='N', max_length=1)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
                'permissions': [('archive_task', 'Archive the task')],
            },
        ),
    ]
