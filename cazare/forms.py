from django import forms
from .models import Rezervare, Problema

class RezervareForm(forms.ModelForm):
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
    class Meta:
        model = Problema
        fields = ['titlu', 'descriere'] # Nu punem 'raportata_de' sau 'rezolvata', astea se pun automat
        widgets = {
            'titlu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Nu merge AC camera 101'}),
            'descriere': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }