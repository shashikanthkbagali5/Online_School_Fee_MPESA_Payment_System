# Generated by Django 2.2.1 on 2019-08-28 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_remove_programme_disp'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='deferred',
            field=models.BooleanField(default=False),
        ),
    ]