from django.urls import path
from . import views

urlpatterns = [
    # Cand adresa e goala (''), cheama functia homepage
    path('', views.homepage, name='acasa'),
]