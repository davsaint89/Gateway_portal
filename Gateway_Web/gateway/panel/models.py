from django.db import models

# Create your models here.
class basic(models.Model):
    SSID = models.CharField(max_length=10)
    contrasena = models.CharField(max_length=15)
    canal = models.CharField(max_length=2)

class advanced(models.Model):
    ip_actual = models.CharField(max_length=20)
    ip_init = models.CharField(max_length=20)
    ip_fin = models.CharField(max_length=20)
    netmask = models.CharField(max_length=20)
    tiempo = models.CharField(max_length=2)

class zigbee(models.Model):
    device = models.CharField(max_length=20)
    pan_id = models.CharField(max_length=20)
    mac_addr=models.CharField(max_length=20)
    baud_rate=models.CharField(max_length=10)
    parity=models.CharField(max_length=5)
    flow_control=models.CharField(max_length=5)
    
class Bluetooth(models.Model):
    mac_addr=models.CharField(max_length=20)
    alias = models.CharField(max_length=20)
    puerto= models.IntegerField()

class PublicBrokerSubscriptor(models.Model):
    topico=models.CharField(max_length=20)
    puerto = models.IntegerField()
    host = models.CharField(max_length=20)
    qos = models.IntegerField()

class PublicBrokerPublisher(models.Model): #
    topico=models.CharField(max_length=20)
    puerto = models.IntegerField()
    host = models.CharField(max_length=20)
    qos = models.IntegerField()

class PrivateBrokerSubscriptor(models.Model):
    topico=models.CharField(max_length=20)
    puerto = models.IntegerField()
    host = models.CharField(max_length=20)
    qos = models.IntegerField()

class PrivateBrokerPublisher(models.Model):
    topico=models.CharField(max_length=20)
    puerto = models.IntegerField()
    host = models.CharField(max_length=20)
    qos = models.IntegerField()






    


