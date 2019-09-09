# Generated by Django 2.2.1 on 2019-08-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('students', '0015_delete_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=100)),
                ('units', models.IntegerField(default=3)),
            ],
        ),
        migrations.AddField(
            model_name='programme',
            name='units',
            field=models.ManyToManyField(blank=True, to='students.Course'),
        ),
    ]
