# Generated by Django 2.2.1 on 2019-09-07 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_transaction_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='api',
            field=models.BooleanField(default=True),
        ),
    ]
