# Generated by Django 2.2.1 on 2019-08-22 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20190821_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='in_session',
            field=models.BooleanField(default=False),
        ),
    ]