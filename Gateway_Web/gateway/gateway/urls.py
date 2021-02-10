"""gateway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from panel import views
from register import views as v
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('broker_privado/',views.broker_privado,name="broker_privado"),
    path('suscriptor/',views.suscriptor,name="suscriptor"),
    path('publisher/',views.publisher,name="publisher"),
    path('broker/',views.broker,name="broker"),
    path('broker_publico/',views.broker_publico,name="broker_pubico"),
    path('estados/', views.state_request,name = "estados"),
    path('estados2/', views.state_request2,name = "estados2"),
    path('estacion_2/', views.ver_estados, name= "estación_2"),
    path('estacion_1/', views.ver_estados2, name= "estación_1"),
    path('actuator/',views.actuator_control,name = "actuator"),
    path('actuator2/',views.actuator_control2,name = "actuator2"),
    path('sensores/',views.sensor_control,name = "sensores"),
    path('sensores2/',views.sensor_control2,name = "sensores2"),
    path('wifi/', views.wifi,name = "wifi"),
    path('bluetooth/',views.bluetooth,name="bluetooth"),
    path('blue_scan/',views.Blue_scan,name = "blue_scan"),
    path('wifi_scan/',views.wifi_scan,name="wifi_scan"),
    path('zigbee/', views.zigbee_vista,name="zigbee"),
    path('administrador/', views.admini,name = "administrador"),
    path('AP_basic_config/',views.AP_basic_config, name="AP_basic_config"),
    path('AP_advanced_config/',views.AP_advanced_config,name="AP_advanced_config"),
    path('zigbee_config/',views.zigbee_config,name = "zigbee_config"),
    path("register/", v.register, name="register"),  # <-- added
    path('', include("django.contrib.auth.urls")),

]

urlpatterns += staticfiles_urlpatterns()

