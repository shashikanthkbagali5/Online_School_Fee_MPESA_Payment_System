# Generated by Django 2.2.1 on 2019-08-24 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_group_in_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='password',
        ),
        migrations.RemoveField(
            model_name='student',
            name='password2',
        ),
    ]
