# Generated by Django 3.0.7 on 2020-08-09 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0004_auto_20200808_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='zigbee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(max_length=20)),
                ('pan_id', models.CharField(max_length=20)),
                ('mac_addr', models.CharField(max_length=20)),
                ('baud_rate', models.CharField(max_length=10)),
                ('parity', models.CharField(max_length=5)),
                ('flow_control', models.CharField(max_length=5)),
            ],
        ),
    ]
