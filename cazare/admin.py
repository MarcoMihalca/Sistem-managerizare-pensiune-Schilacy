from django.contrib import admin
from .models import Utilizator, Client, TipCamera, Camera, Rezervare, Factura, Problema

# Înregistrăm modelele pentru a le vedea în panoul de admin
admin.site.register(Utilizator)
admin.site.register(Client)
admin.site.register(TipCamera)
admin.site.register(Camera)
admin.site.register(Rezervare)
admin.site.register(Factura)
admin.site.register(Problema)