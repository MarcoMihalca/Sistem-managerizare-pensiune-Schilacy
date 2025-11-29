import os
import django
from pdoc import pdoc
from pathlib import Path  # <--- Am adaugat importul asta

# 1. Spunem scriptului unde sunt setarile Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PensiuneaSchilacy.settings')

# 2. Pornim Django (incarcam aplicatiile)
django.setup()

# 3. Generam documentatia
print("Generare documentatie in curs...")

# <--- Aici folosim Path('./docs') in loc de './docs' simplu
pdoc('cazare', output_directory=Path('./docs'))

print("Gata! Verifica folderul 'docs'.")