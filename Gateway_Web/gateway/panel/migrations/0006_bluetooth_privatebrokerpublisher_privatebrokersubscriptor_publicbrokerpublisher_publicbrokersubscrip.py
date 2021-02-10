# Generated by Django 3.0.8 on 2020-11-08 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0005_zigbee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bluetooth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_addr', models.CharField(max_length=20)),
                ('alias', models.CharField(max_length=20)),
                ('puerto', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PrivateBrokerPublisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topico', models.CharField(max_length=20)),
                ('puerto', models.IntegerField()),
                ('host', models.CharField(max_length=20)),
                ('qos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PrivateBrokerSubscriptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topico', models.CharField(max_length=20)),
                ('puerto', models.IntegerField()),
                ('host', models.CharField(max_length=20)),
                ('qos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PublicBrokerPublisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topico', models.CharField(max_length=20)),
                ('puerto', models.IntegerField()),
                ('host', models.CharField(max_length=20)),
                ('qos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PublicBrokerSubscriptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topico', models.CharField(max_length=20)),
                ('puerto', models.IntegerField()),
                ('host', models.CharField(max_length=20)),
                ('qos', models.IntegerField()),
            ],
        ),
    ]
