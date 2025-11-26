from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilizator, Client, TipCamera, Camera, Rezervare, Factura, Problema

# Definim o clasa speciala pentru Admin care stie sa gestioneze parolele
class UtilizatorAdmin(UserAdmin):
    # Aici ii spunem sa adauge campul 'rol' in formularul de editare, pe langa cele standard
    fieldsets = UserAdmin.fieldsets + (
        ('Roluri Personalizate', {'fields': ('rol',)}),
    )
    # Aici ii spunem sa adauge 'rol' si la formularul de creare utilizator nou
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Roluri Personalizate', {'fields': ('rol',)}),
    )

# Inregistram modelul Utilizator folosind clasa speciala de mai sus
admin.site.register(Utilizator, UtilizatorAdmin)

# Restul modelelor raman la fel
admin.site.register(Client)
admin.site.register(TipCamera)
admin.site.register(Camera)
admin.site.register(Rezervare)
admin.site.register(Factura)
admin.site.register(Problema)