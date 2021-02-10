from django.shortcuts import render
from panel.models import advanced, basic, zigbee, PrivateBrokerPublisher, PrivateBrokerSubscriptor, PublicBrokerPublisher,PublicBrokerSubscriptor
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import sqlite3
import json
import os
from django.utils import timezone
import shutil
from django.http import JsonResponse
from configparser import ConfigParser
from datetime import date, datetime, time, timedelta
#import bluetooth
#import os

# Create your views here.
global time_control
Gateway_IP = "192.168.4.1"
passd = "Piico2020*"
chan = "7"
Name = "S-PIICO"
time_control = 0 



def broker_privado(request):

    with open('/home/pi/Documents/comunicacion/conf_l.json', 'r') as file:
        data_conf = json.load(file)
        top2 = data_conf['broker']['suscribe'][0]['topic_1']
        top3 = data_conf['broker']['suscribe'][1]['topic_2']
        top4 = data_conf['broker']['suscribe'][2]['topic_3']
        top = data_conf['broker']['publish'][0]['topic_4']
        top1 = data_conf['broker']['publish'][1]['topic_5']
        host = data_conf['broker']['broker_address']
        port = data_conf['broker']['port']
        qos = data_conf['broker']['qos']

    return render(request, "panel/brokerPriv.html",{'t1':top,'p1':port,'h1':host,'q1':qos,'t2':top1,'p2':port,'h2':host,'q2':qos,'t3':top2,'p3':port,'h3':host,'q3':qos,'t4':top3,'p4':port,'h4':host,'q4':qos,'t5':top4,'p5':port,'h5':host,'q5':qos})

def suscriptor(request):
    
    with open('/home/pi/Documents/comunicacion/conf_l.json','r') as file:
        data_conf = json.load(file)
    
    if request.method == 'POST':
        name = request.POST["nombre"]
        name1 = request.POST["nombre1"]
        name2 = request.POST["nombre2"]
        
        with open('/home/pi/Documents/comunicacion/conf_l.json','w') as file:
            data_conf['broker']['suscribe'][0]['topic_1'] = name
            data_conf['broker']['suscribe'][1]['topic_2'] = name1
            data_conf['broker']['suscribe'][2]['topic_3'] = name2
            json.dump(data_conf,file)
    
    #return render(request, 'panel/brokerPriv.html')
def publisher(request):
    
    with open('/home/pi/Documents/comunicacion/conf_l.json','r') as file:
        data_conf = json.load(file)
    
    if request.method == 'POST':
        name = request.POST["nombre2"]
        name1 = request.POST["nombre3"]
        
        
        with open('/home/pi/Documents/comunicacion/conf_l.json','w') as file:
            data_conf['broker']['publish'][0]['topic_4'] = name
            data_conf['broker']['publish'][1]['topic_5'] = name1
            json.dump(data_conf,file)
            
def broker(request):
    
    with open('/home/pi/Documents/comunicacion/conf_l.json','r') as file:
        data_conf = json.load(file)
    
    if request.method == 'POST':
        port = request.POST["port"]
        qos = request.POST["qos"]
        
        with open('/home/pi/Documents/comunicacion/conf_l.json','w') as file:
            data_conf['broker']['port'] = port
            data_conf['broker']['qos'] = qos
            json.dump(data_conf,file)


def broker_publico(request):

    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    config = cur.execute("select *from 'panel_PublicBrokerPublisher'").fetchall()[-1] # retorno una tupla    
    top = config[1]
    port = config[2]
    host = config[3]
    qos = config[4]

    config1 = cur.execute("select *from 'panel_PublicBrokerPublisher'").fetchall()[-2]
    top1 = config1[1]
    port1 = config1[2]
    host1 = config1[3]
    qos1 = config1[4] 

    config2 = cur.execute("select *from 'panel_PublicBrokerSubscriptor'").fetchall()[-1]
    top2 = config2[1]
    port2 = config2[2]
    host2 = config2[3]
    qos2 = config2[4] 

    config3 = cur.execute("select *from 'panel_PublicBrokerSubscriptor'").fetchall()[-2]
    top3 = config3[1]
    port3 = config3[2]
    host3 = config3[3]
    qos3 = config3[4]

    config4 = cur.execute("select *from 'panel_PublicBrokerSubscriptor'").fetchall()[-3]
    top4 = config4[1]
    port4 = config4[2]
    host4 = config4[3]
    qos4 = config4[4]

    if request.method == 'POST':

        topico1 = request.POST["topico1"]
        puerto1 = request.POST["puerto1"]
        host1 = request.POST["host1"]
        qos1 = request.POST["qos1"]
        subs = PublicBrokerSubscriptor(topico=topico1,puerto=puerto1,host=host1,qos=qos1)
        subs.save()   

    return render(request, "panel/brokerPub.html",{'t1':top,'p1':port,'h1':host,'q1':qos,'t2':top1,'p2':port1,'h2':host1,'q2':qos1,'t3':top2,'p3':port2,'h3':host2,'q3':qos2,'t4':top3,'p4':port3,'h4':host3,'q4':qos3,'t5':top4,'p5':port4,'h5':host4,'q5':qos4})

def index(request):

    return render(request, 'panel/frontpage.html')


def ver_estados(request):
    global time_control, control_cambio
    per = 0
    from datetime import date, datetime, time, timedelta
    lista = []
    
    with open('/home/pi/Documents/comunicacion/data.json') as file:
        data = json.load(file) # retorna un diccionario
        fecha = data['date']
        period = data['nodes'][0]['sampling_period']
        per = round(60/(int(period)/60))
        #time_comp = datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S")
        #aux = datetime.timestamp(time_comp)
        #control_cambio = round(aux)
        #print("control_cambio",control_cambio)
        node = data['nodes'][0]['node_id']
        #if control_cambio > time_control:
            #time_control = control_cambio
        #    stat = 'Offline'
        #elif control_cambio <= time_control:
        stat = data['nodes'][0]['state']
        for sensor in data['nodes'][0]['sensors']:
            if sensor['sensor_id'] == 'Temperature':
                a = "AM2315"
                b = "Temperatura"
                clase = "Sensor"
                if sensor['on'] == "True":
                    c = "Online"
                else:
                    c = "Offline"

            if sensor['sensor_id'] == 'Humidity':
                d = "AM2315"
                e = "Humedad"
                clase1 = "Sensor"
                if sensor['on'] == "True":
                    f = "Online"
                else:
                    f = "Offline"

            if sensor['sensor_id'] == 'Velocity':
                g = "SEN-08942-anemómetro"
                h = "Velocidad del viento"
                clase2 = "Sensor"
                if sensor['on'] == "True":
                    i = "Online"
                else:
                    i = "Offline"

            if sensor['sensor_id'] == 'Direction':
                j = "SEN-08942-veleta"
                k = "Direccion del viento"
                clase3 = "Sensor"
                if sensor['on'] == "True":
                    l = "Online"
                else:
                    l = "Offline"

            if sensor['sensor_id'] == 'Radiation':
                m = "Davis 6450"
                n = "Radiación solar"
                clase4 = "Sensor"
                if sensor['on'] == "True":
                    o = "Online"
                else:
                    o = "Offline"

            if sensor['sensor_id'] == 'Pluviometer':
                p = "SEN-08942-pluviometro"
                q = "Pluviometría"
                clase5 = "Sensor"
                if sensor['on'] == "True":
                    r = "Online"
                else:
                    r = "Offline"
        for actuador in data['nodes'][0]['actuators']:
            if actuador['actuator_id'] == 'Lawn_sprinkler':
                s = "Aspersor de agua"
                t = "Irrigación"
                clase6 = "actuador"
                if actuador['valvula'] == 'on':
                    u = "Encendido"
                else:
                    u= "Apagado"

        return render(request, 'panel/index.html',{'freq':per,'node':node,'stat':stat,'fecha':fecha,'dev':a,'tipo':b,'est':c,'clase':clase,'dev1':d,'tipo1':e,'est1':f,'clase1':clase1,'dev2':g,'tipo2':h,'est2':i,'clase2':clase2,'dev3':j,'tipo3':k,'est3':l,'clase3':clase3,'dev4':m,'tipo4':n,'est4':o,'clase4':clase4,'dev5':p,'tipo5':q,'est5':r,'clase5':clase5,'dev6':s,'tipo6':t,'est6':u,'clase6':clase6})

def ver_estados2(request):

    lista = []
    with open('/home/pi/Documents/comunicacion/data1.json') as file:
        data = json.load(file) # retorna un diccionario
        fecha = data['date']
        node = data['nodes'][0]['node_id']
        stat = data['nodes'][0]['state']
        period = data['nodes'][0]['sampling_period']
        per = round(60/(int(period)/60))
        for sensor in data['nodes'][0]['sensors']:
            if sensor['sensor_id'] == 'Temperature':
                a = "AM2315"
                b = "Temperatura"
                clase = "Sensor"
                if sensor['on'] == "True":
                    c = "Online"
                else:
                    c = "Offline"

            if sensor['sensor_id'] == 'Humidity':
                d = "AM2315"
                e = "Humedad"
                clase1 = "Sensor"
                if sensor['on'] == "True":
                    f = "Online"
                else:
                    f = "Offline"

            if sensor['sensor_id'] == 'Velocity':
                g = "SEN-08942-anemómetro"
                h = "Velocidad del viento"
                clase2 = "Sensor"
                if sensor['on'] == "True":
                    i = "Online"
                else:
                    i = "Offline"

            if sensor['sensor_id'] == 'Direction':
                j = "SEN-08942-veleta"
                k = "Direccion del viento"
                clase3 = "Sensor"
                if sensor['on'] == "True":
                    l = "Online"
                else:
                    l = "Offline"

            if sensor['sensor_id'] == 'Radiation':
                m = "Davis 6450"
                n = "Radiación solar"
                clase4 = "Sensor"
                if sensor['on'] == "True":
                    o = "Online"
                else:
                    o = "Offline"

            if sensor['sensor_id'] == 'Pluviometer':
                p = "SEN-08942-pluviometro"
                q = "Pluviometría"
                clase5 = "Sensor"
                if sensor['on'] == "True":
                    r = "Online"
                else:
                    r = "Offline"
        for actuador in data['nodes'][0]['actuators']:
            if actuador['actuator_id'] == 'Lawn_sprinkler':
                s = "Aspersor de agua"
                t = "Irrigación"
                clase6 = "actuador"
                if actuador['valvula'] == 'on':
                    u = "Encendido"
                else:
                    u= "Apagado"

        return render(request, 'panel/control.html',{'per':per,'node':node,'stat':stat,'fecha':fecha,'dev':a,'tipo':b,'est':c,'clase':clase,'dev1':d,'tipo1':e,'est1':f,'clase1':clase1,'dev2':g,'tipo2':h,'est2':i,'clase2':clase2,'dev3':j,'tipo3':k,'est3':l,'clase3':clase3,'dev4':m,'tipo4':n,'est4':o,'clase4':clase4,'dev5':p,'tipo5':q,'est5':r,'clase5':clase5,'dev6':s,'tipo6':t,'est6':u,'clase6':clase6})


def state_request(request):
    from datetime import date, datetime, time, timedelta
    
    cinco_horas = timedelta(hours=5) 
    hoy= datetime.today()
    fecha_actual = hoy - cinco_horas
    time_c = datetime.timestamp(fecha_actual)
    formatdate= "%d/%m/%Y %H:%M:%S"
    now = fecha_actual.strftime(formatdate)
    time_control = round(time_c)
    print("time_control",time_control)
    req_info = {}
    info = {}
    req_info['node_id'] = "estacion_2"
    req_info['pass'] = "1234" #request.POST["pass"]
    req_info['request'] = "info"
    req_info['date'] = now 
    req_info['information'] = {}
    req_info['information']['location'] = "true"
    req_info['information']['node'] = "true"
    req_info['information']['interfaces'] = "true"
    req_info['information']['actuators'] = request.POST["actuador"]#"true"#
    req_info['information']['sensors'] = request.POST["sensor"]#"true"#request.POST["sensor"]
    req_info['information']['mqtt'] = "true"
    string_message = json.dumps(req_info)
    publish.single("req_l", string_message, hostname="192.168.4.1")
    ver_estados()
    #return render(request, 'panel/index.html')
    
def state_request2(request):
    from datetime import date, datetime, time, timedelta
    
    hoy= datetime.today()
    formatdate= "%d/%m/%Y %H:%M:%S"
    now = hoy.strftime(formatdate)

    req_info = {}
    info = {}
    req_info['node_id'] = "estacion_1"
    req_info['pass'] = "1234" #request.POST["pass"]
    req_info['request'] = "info"
    req_info['date'] = now 
    req_info['information'] = {}
    req_info['information']['location'] = "true"
    req_info['information']['node'] = "true"
    req_info['information']['interfaces'] = "true"
    req_info['information']['actuators'] = request.POST["actuador"]#"true"#
    req_info['information']['sensors'] = request.POST["sensor"]#"true"#request.POST["sensor"]
    req_info['information']['mqtt'] = "true"
    string_message = json.dumps(req_info)
    publish.single("req_l", string_message, hostname="192.168.4.1")

    return render(request, 'panel/control.html')

def actuator_control(request):

    config_string = {}
    config_string['node_id'] = "estacion_2"
    config_string['pass'] = "1234" #
    config_string['request'] = "act"
    config_string['actuators'] = []
    actuador = {}
    actuador['actuator_id'] = request.POST["actuator-id"]
    actuador['order'] = request.POST["order"]
    config_string['actuators'].append(actuador)
    new_string = json.dumps(config_string, indent=2, sort_keys=False)
    publish.single("act_l",new_string, hostname="192.168.4.1")
    #return render(request, "panel/index.html")
    
def actuator_control2(request):

    config_string = {}
    config_string['node_id'] = "estacion_1"
    config_string['pass'] = "1234" #
    config_string['request'] = "act"
    config_string['actuators'] = []
    actuador = {}
    actuador['actuator_id'] = request.POST["actuator-id"]
    actuador['order'] = request.POST["order"]
    config_string['actuators'].append(actuador)
    new_string = json.dumps(config_string, indent=2, sort_keys=False)
    publish.single("act_l",new_string, hostname="192.168.4.1")
    return render(request, "panel/control.html")
    

def sensor_control(request):

    sensor_string = {}
    sensor_string['node_id'] = "estacion_2"
    entrada = request.POST["request1"]
    time = request.POST["minutos"]
    tiempo = int(time)*60   
    sensor_string['sample_period'] = tiempo
    sensor_string['request'] = entrada
    sensor_string['sensors'] = []
    sensor_string['protocols'] = []
    protocol1 = {}
    protocol2 = {}
    protocol3 = {}
    sensor1 = {}
    sensor2 = {}
    sensor3 = {}
    sensor4 = {}
    sensor5 = {}
    sensor6 = {}
    sensor1['sensor_id'] = request.POST["sensor1"]
    sensor2['sensor_id'] = request.POST["sensor2"]
    sensor3['sensor_id'] = request.POST["sensor3"]
    sensor4['sensor_id'] = request.POST["sensor4"]
    sensor5['sensor_id'] = request.POST["sensor5"]
    sensor6['sensor_id'] = request.POST["sensor6"]
    protocol1['network'] = request.POST["protocol-1"]
    protocol2['network'] = request.POST["protocol-2"]
    protocol3['network'] = request.POST["protocol-3"]
    sensor_string['sensors'].append(sensor1)
    sensor_string['sensors'].append(sensor2)
    sensor_string['sensors'].append(sensor3)
    sensor_string['sensors'].append(sensor4)
    sensor_string['sensors'].append(sensor5)
    sensor_string['sensors'].append(sensor6)
    sensor_string['protocols'].append(protocol1)
    sensor_string['protocols'].append(protocol2)
    sensor_string['protocols'].append(protocol3)

    carga = json.dumps(sensor_string, indent=2, sort_keys=False)
    publish.single("req_l",carga, hostname="192.168.4.1")
    return render(request, 'panel/index.html')
    
def sensor_control2(request):

    sensor_string = {}
    sensor_string['node_id'] = "estacion_1"
    sensor_string['request'] = request.POST["request1"]
    sensor_string['sensors'] = []
    sensor_string['protocols'] = []
    protocol1 = {}
    protocol2 = {}
    protocol3 = {}
    sensor1 = {}
    sensor2 = {}
    sensor3 = {}
    sensor4 = {}
    sensor5 = {}
    sensor6 = {}
    sensor1['sensor_id'] = request.POST["sensor1"]
    sensor2['sensor_id'] = request.POST["sensor2"]
    sensor3['sensor_id'] = request.POST["sensor3"]
    sensor4['sensor_id'] = request.POST["sensor4"]
    sensor5['sensor_id'] = request.POST["sensor5"]
    sensor6['sensor_id'] = request.POST["sensor6"]
    protocol1['network'] = request.POST["protocol-1"]
    protocol2['network'] = request.POST["protocol-2"]
    protocol3['network'] = request.POST["protocol-3"]
    sensor_string['sensors'].append(sensor1)
    sensor_string['sensors'].append(sensor2)
    sensor_string['sensors'].append(sensor3)
    sensor_string['sensors'].append(sensor4)
    sensor_string['sensors'].append(sensor5)
    sensor_string['sensors'].append(sensor6)
    sensor_string['protocols'].append(protocol1)
    sensor_string['protocols'].append(protocol2)
    sensor_string['protocols'].append(protocol3)

    carga = json.dumps(sensor_string, indent=2, sort_keys=False)
    publish.single("req_l",carga, hostname="192.168.4.1")
    return render(request, 'panel/control.html')
    


def wifi(request):
    
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    config = cur.execute("select *from 'panel_basic'").fetchall()[-1] # retorno una tupla    
    SSID = config[1]
    contrasena = config[2]
    canal = config[3]

    con2 = sqlite3.connect('db.sqlite3')
    cur2 = con2.cursor()
    config2 = cur2.execute("select *from 'panel_advanced'").fetchall()[-1]
    ip_actual = config2[1]
    ip_init = config2[2]
    ip_fin = config2[3]
    netmask = config2[4]
    time = config2[5] 
    
    return render(request, "panel/wifi.html",{'SSID':SSID,'ip_actual':ip_actual,'contrasena':contrasena,'canal':canal,'netmask':netmask,'ip_init':ip_init,'ip_fin':ip_fin,'time':time})

def wifi_scan(request):
    import socket
    import time


    nodos = []
    net = Gateway_IP
    net1 = net.split('.')
    a = '.'

    net2 = net1[0] + a + net1[1] + a + net1[2] + a
    st1 = 2
    en1 = 25 
    en1 = en1 + 1
    t1 = time.perf_counter()

    def scan(addr):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((addr,22))
        if result == 0:
            return 1
        else :
            return 0

    def run1():
        for ip in range(st1,en1):
            addr = net2 + str(ip)
            if (scan(addr)):
                ver = str(addr + " online")
                nodos.append(ver)
    run1()
    t2 = time.perf_counter()
    total = str(round(t2 - t1, 2)) + " segundos"
    return render(request,'panel/wifi2.html',{'nodos':nodos, 'tiempo':total})

def avanzado(current, address, dirIni, dirFin, time, netmask): ##esta no es una vista
    original = r'/home/pi/Documents/wifi.ini'
    target = r'/home/pi/Documents/hostapd.conf'
    nOriginal = r'/home/pi/Documents/dns.ini'
    target1 = r'/home/pi/Documents/dnsmasq.conf'
    base = r'/home/pi/Documents/dhcpcd.ini'
    destino = r'/home/pi/Documents/dhcpcd.conf'

    file1 = '/home/pi/Documents/dns.ini'
    config1 = ConfigParser()
    config1.read(file1)

    file = '/home/pi/Documents/wifi.ini'
    config = ConfigParser()
    config.read(file)
    tiempo = time
    direccion = ("/gw.wlan/" + address)
    original = current + "/24"
    print(original)
    nueva = address + "/24"
    print(nueva)
    rango = (dirIni+","+dirFin+"," + netmask +","+tiempo)
    config1.set('rango','dhcp-range',rango)
    config1.set('rango','address',direccion)
    with open(file1, 'w') as configfile:
        config1.write(configfile)
    shutil.copy(nOriginal,target1)
    
    b_file = open("/home/pi/Documents/dnsmasq.conf", "r+")
    lineas = b_file.readlines()
    b_file.close()
    del lineas[0]  

    new1_file = open("/home/pi/Documents/dnsmasq.conf", "w+")
    for linea in lineas:
        p = linea.replace(" ","")
        new1_file.write(p)
    new1_file.close()
    os.system("sudo cp /home/pi/Documents/dnsmasq.conf /etc/dnsmasq.conf")
    
    c_file = open("/home/pi/Documents/dhcpcd.ini", "r+")
    lineas = c_file.readlines()
    c_file.close()

    new_file = open("/home/pi/Documents/dhcpcd.ini", "w+")
    for linea in lineas:
        p = linea.replace(original,nueva)
        new_file.write(p)
    new_file.close()
    shutil.copy(base, destino) 
    os.system("sudo cp /home/pi/Documents/dhcpcd.conf /etc/dhcpcd.conf")

def AP_basic_config(request):
    from configparser import ConfigParser
    import shutil

    original = r'/home/pi/Documents/wifi.ini'
    target = r'/home/pi/Documents/hostapd.conf'
    SSID = request.POST["SSID"]
    passwd = request.POST["passwd"]
    channel = request.POST["channel"]

    file = '/home/pi/Documents/wifi.ini'
    config = ConfigParser()
    config.read(file)
    config.set('configuration', 'ssid',SSID)
    config.set('configuration', 'wpa_passphrase',passwd)
    config.set('configuration', 'channel',channel)
    with open(file, 'w') as configfile:
        config.write(configfile)
    shutil.copy(original, target)
    a_file = open("/home/pi/Documents/hostapd.conf", "r+")
    lines = a_file.readlines()
    a_file.close()
    del lines[0]
    new_file = open("/home/pi/Documents/hostapd.conf", "w+")
    for line in lines:
        c = line.replace(" ","")
        new_file.write(c)
    new_file.close()
    os.system("sudo cp /home/pi/Documents/hostapd.conf /etc/hostapd.conf")
    AP_basic = basic(SSID=SSID,contrasena=passwd,canal=channel)
    AP_basic.save()
    
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    config = cur.execute("select *from 'panel_basic'").fetchall()[-1] # retorno una tupla
    SSID = config[1]
    contrasena = config[2]
    canal = config[3]

    archivo = open('/home/pi/Documents/comunicacion/conf_l.json','r')
    data_conf = json.load(archivo)
    archivo.close()
    data_conf['interfaces'][0]['ssid'] = SSID
    data_conf['interfaces'][0]['psk'] = contrasena
    archivo = open('/home/pi/Documents/comunicacion/conf_l.json','w')
    json.dump(data_conf,archivo)
    archivo.close()

    con2 = sqlite3.connect('db.sqlite3')
    cur2 = con2.cursor()
    config2 = cur2.execute("select *from 'panel_advanced'").fetchall()[-1]
    ip_actual = config2[1]
    ip_init = config2[2]
    ip_fin = config2[3]
    netmask = config2[4]
    time = config2[5]
    publish.single("conf_l", data_conf, hostname="192.168.4.1")
    #os.system("sudo reboot")

    return render(request, "panel/wifi.html",{'SSID':SSID,'ip_actual':ip_actual,'contrasena':contrasena,'canal':canal,'netmask':netmask,'ip_init':ip_init,'ip_fin':ip_fin,'time':time})

def AP_advanced_config(request):
    if request.method == 'POST':
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        config = cur.execute("select *from 'panel_advanced'").fetchall()[-1]
        current = config[1]

        ip_nueva = request.POST["ip_nueva"]
        ip_init = request.POST["ip_init"]
        ip_fin = request.POST["ip_fin"]
        netmask = request.POST["netmask"]
        time = "24h"
        AP_advanced = advanced(ip_actual=ip_nueva,ip_init=ip_init,ip_fin=ip_fin,netmask=netmask,tiempo=time)
        AP_advanced.save()
        

        config = cur.execute("select *from 'panel_basic'").fetchall()[-1] # retorna una tupla    
        SSID = config[1]
        contrasena = config[2]
        canal = config[3]

        
        config2 = cur.execute("select *from 'panel_advanced'").fetchall()[-1]
        ip_actual = config2[1]
        ip_init = config2[2]
        ip_fin = config2[3]
        netmask = config2[4]
        time = config2[5]

        avanzado(current,ip_actual,ip_init,ip_fin,time,netmask)

        archivo = open('/home/pi/Documents/comunicacion/conf_l.json','r')
        data_conf = json.load(archivo)
        archivo.close()
        data_conf['broker']['broker_address'] = ip_actual
        archivo = open('/home/pi/Documents/comunicacion/conf_l.json','w')
        json.dump(data_conf,archivo)
        archivo.close()
        publish.single("conf_l", data_conf, hostname="192.168.4.1")
        #os.system("sudo reboot")

        
        return render(request, "panel/wifi.html",{'SSID':SSID,'ip_actual':ip_actual,'contrasena':contrasena,'canal':canal,'netmask':netmask,'ip_init':ip_init,'ip_fin':ip_fin,'time':time})
    else:
        return render(request,"panel/wifi.html")
        
def bluetooth(request):

    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    config = cur.execute("select *from 'panel_bluetooth'").fetchall()[-1]
    mac = config[1]
    device = config[2]

    with open('/home/pi/Documents/comunicacion/conf_l.json','r') as archivo:
        data_conf = json.load(archivo)
        port = data_conf['interfaces'][1]['port']
    
    if request.method == 'POST':
        puerto = request.POST["port"]
        with open('/home/pi/Documents/comunicacion/conf_l.json','w') as archivo:
            data_conf['interfaces'][1]['port'] = puerto
            json.dump(data_conf,archivo)
        

    return render(request, "panel/bluetooth.html",{"device":device,"mac":mac,"port":port})

def Blue_scan(request):

    import bluetooth
    import os

    devices = []
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                                            flush_cache=True, lookup_class=False)
    num_dev = str(len(nearby_devices))
    for addr, name in nearby_devices:
        dev = str("   {} - {}".format(addr, name))
        devices.append(dev)

    return render(request, "panel/bluetooth2.html",{"cantidad":num_dev,"aparatos": devices})

def zigbee_vista(request):

    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    xbee = cur.execute("select *from 'panel_zigbee'").fetchall()[-1] # retorno una tupla    
    dev = xbee[1]
    pan = xbee[2]
    mac_a = xbee[3]
    bau = xbee[4]
    par = xbee[5]
    flo = xbee[6]

    return render(request, "panel/zigbee.html",{'device':dev,'pan_id':pan,'mac_address':mac_a,'bauds':bau,'parity':par,'flow_control':flo})
    
def admini(request):
    return render(request, "panel/administrator.html")

def zigbee_config(request):

    device = request.POST["device"]
    pan_id = request.POST["pan_id"]
    mac = request.POST["mac"]
    baud = request.POST["bauds"]
    paridad = request.POST["parity"]
    flow = request.POST["flow_control"]

    XBEE = zigbee(device=device, pan_id=pan_id, mac_addr=mac, baud_rate=baud, parity=paridad, flow_control=flow)
    XBEE.save()

    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    xbee = cur.execute("select *from 'panel_zigbee'").fetchall()[-1] # retorno una tupla    
    dev = xbee[1]
    pan = xbee[2]
    mac_a = xbee[3]
    bau = xbee[4]
    par = xbee[5]
    flo = xbee[6]

    return render(request, "panel/zigbee.html",{'device':dev,'pan_id':pan,'mac_address':mac_a,'bauds':bau,'parity':par,'flow_control':flo})

    
