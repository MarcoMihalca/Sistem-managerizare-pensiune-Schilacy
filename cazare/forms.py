from django import forms
from .models import Rezervare

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