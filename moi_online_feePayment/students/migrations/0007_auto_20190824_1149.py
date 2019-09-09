# Generated by Django 2.2.1 on 2019-08-24 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20190824_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programme', models.CharField(max_length=200)),
                ('disp', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='programme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Programme'),
        ),
    ]