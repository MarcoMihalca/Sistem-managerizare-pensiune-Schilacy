from django.apps import AppConfig

"""
Configurarea Aplicației (App Configuration).

Acest modul definește setările de bază pentru aplicația 'cazare', cum ar fi
tipul implicit pentru cheile primare (Auto Field) și numele intern al aplicației.
Aceste setări sunt încărcate automat de Django la pornirea serverului.
"""

class CazareConfig(AppConfig):
    """
    Clasa de configurare principală pentru aplicația 'cazare'.
    
    Attributes:
        default_auto_field (str): Tipul de câmp folosit implicit pentru ID-uri (BigAuto).
        name (str): Numele tehnic al aplicației (folosit în INSTALLED_APPS).
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cazare'
