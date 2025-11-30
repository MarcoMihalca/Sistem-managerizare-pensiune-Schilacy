from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

"""
Configurarea Rutelor URL.

Acest modul funcționează ca o "hartă" a site-ului. Leagă adresele accesate
de utilizator în browser (ex: '/rezervari/') de funcțiile Python corespunzătoare
din 'views.py'.

Rute Principale:
- / : Dashboard-ul principal (homepage).
- /login & /logout : Sistemul de autentificare.
- /rezervare-noua/ : Formularul de creare rezervări.
- /rezervare/checkout/... : Procesul de finalizare și facturare.
- /rapoarte/ : Zona de statistici pentru manageri.
"""

urlpatterns = [
    # Cand adresa e goala (''), cheama functia homepage
    path('', views.homepage, name='acasa'),
    path('login/', auth_views.LoginView.as_view(template_name='cazare/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('rezervare-noua/', views.creare_rezervare, name='creare_rezervare'),
    path('rezervari/', views.lista_rezervari, name='lista_rezervari'),
    path('rezervare/anulare/<int:rezervare_id>/', views.anuleaza_rezervare, name='anuleaza_rezervare'),
    # ... celelalte rute ...
    path('rezervare/checkout/<int:rezervare_id>/', views.efectueaza_check_out, name='efectueaza_check_out'),
    path('factura/<int:factura_id>/', views.vizualizare_factura, name='vizualizare_factura'),
    path('rapoarte/', views.rapoarte_manager, name='rapoarte_manager'),
    # ... rute existente ...
    path('raporteaza/', views.raporteaza_problema, name='raporteaza_problema'),
    path('probleme/', views.lista_probleme, name='lista_probleme'),
    path('probleme/rezolva/<int:problema_id>/', views.rezolva_problema, name='rezolva_problema'),
]