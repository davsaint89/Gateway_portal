# Generated by Django 3.0.7 on 2020-08-08 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_auto_20200808_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuracion',
            name='ip_nueva',
        ),
    ]
