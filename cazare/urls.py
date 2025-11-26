from django.urls import path
from . import views

urlpatterns = [
    # Cand adresa e goala (''), cheama functia homepage
    path('', views.homepage, name='acasa'),
    path('rezervare-noua/', views.creare_rezervare, name='creare_rezervare'),
    path('rezervari/', views.lista_rezervari, name='lista_rezervari'),
    path('rezervare/anulare/<int:rezervare_id>/', views.anuleaza_rezervare, name='anuleaza_rezervare'),
]