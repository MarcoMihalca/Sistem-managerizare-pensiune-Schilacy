from django import forms
from .models import Rezervare, Problema

"""
Modulul Forms pentru validarea și procesarea datelor de intrare.

Acest modul definește formularele Django utilizate pentru a
colecta și valida datele introduse de utilizatori în interfață.
Include configurări pentru widget-uri HTML specifice (ex: calendare datepicker).
"""

class RezervareForm(forms.ModelForm):
    """
    Formular pentru gestionarea datelor unei rezervări.

    Facilități:
        - Widget-uri personalizate 'DateInput' pentru selecția vizuală a datelor (calendar).
        - Validare automată a câmpurilor pe baza modelului Rezervare.
    """
    class Meta:
        model = Rezervare
        # Specificam campurile pe care le completeaza userul
        fields = ['client', 'camere', 'data_check_in', 'data_check_out', 'status']
        
        # Aici facem ca datele sa aiba un calendar dragut (datepicker)
        widgets = {
            'data_check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class ProblemaForm(forms.ModelForm):
    """
    Formular simplificat pentru raportarea problemelor tehnice.

    Este utilizat de personal pentru a descrie defecțiunile observate.
    Câmpurile administrative (cine a raportat, data) sunt excluse și completate automat.
    """
    class Meta:
        model = Problema
        fields = ['titlu', 'descriere'] # Nu punem 'raportata_de' sau 'rezolvata', astea se pun automat
        widgets = {
            'titlu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Nu merge AC camera 101'}),
            'descriere': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }