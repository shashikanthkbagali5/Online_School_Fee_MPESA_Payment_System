# Generated by Django 2.2.1 on 2019-08-30 10:31

from django.db import migrations


class Migration(migrations.Migration):

    atomic = False
    dependencies = [
        ('students', '0012_auto_20190830_1328'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Courses',
            new_name='Course',
        ),
    ]