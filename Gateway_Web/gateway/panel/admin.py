from django.contrib import admin
from panel.models import basic, advanced, zigbee


# Register your models here.
admin.site.register(basic)
admin.site.register(advanced)
admin.site.register(zigbee)
