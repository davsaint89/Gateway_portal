# Generated by Django 3.0.7 on 2020-08-08 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='configuracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SSID', models.CharField(max_length=10)),
                ('contrasena', models.CharField(max_length=15)),
                ('canal', models.CharField(max_length=2)),
                ('ip_actual', models.CharField(max_length=20)),
                ('ip_nueva', models.CharField(max_length=20)),
                ('ip_init', models.CharField(max_length=20)),
                ('ip_fin', models.CharField(max_length=20)),
                ('netmask', models.CharField(max_length=20)),
                ('tiempo', models.CharField(max_length=2)),
            ],
        ),
        migrations.DeleteModel(
            name='avanzado',
        ),
        migrations.DeleteModel(
            name='basico',
        ),
    ]
