from django.urls import path
from . import views

urlpatterns = [
    # Cand adresa e goala (''), cheama functia homepage
    path('', views.homepage, name='acasa'),
    path('rezervare-noua/', views.creare_rezervare, name='creare_rezervare'),
    path('rezervari/', views.lista_rezervari, name='lista_rezervari'),
    path('rezervare/anulare/<int:rezervare_id>/', views.anuleaza_rezervare, name='anuleaza_rezervare'),
    # ... celelalte rute ...
    path('rezervare/checkout/<int:rezervare_id>/', views.efectueaza_check_out, name='efectueaza_check_out'),
    path('factura/<int:factura_id>/', views.vizualizare_factura, name='vizualizare_factura'),
    path('rapoarte/', views.rapoarte_manager, name='rapoarte_manager'),
]