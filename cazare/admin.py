from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilizator, Client, TipCamera, Camera, Rezervare, Factura, Problema

"""
Configurarea Interfeței de Administrare (Django Admin).

Acest modul definește modul în care modelele sunt afișate în panoul de control.
Include o personalizare majoră pentru modelul 'Utilizator', permițând administratorilor
să seteze roluri (Manager/Recepționer) direct din interfață.
"""

# Definim o clasa speciala pentru Admin care stie sa gestioneze parolele
class UtilizatorAdmin(UserAdmin):
    """
    Personalizarea panoului de administrare pentru utilizatori.

    Deoarece folosim un model de user personalizat (care are câmpul extra 'rol'),
    trebuie să modificăm formularele standard din Django Admin pentru a include
    acest câmp la creare și editare.

    Modificări:
        - fieldsets: Adaugă secțiunea 'Roluri Personalizate' în pagina de editare user.
        - add_fieldsets: Adaugă câmpul 'rol' în pagina de creare user nou.
    """
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