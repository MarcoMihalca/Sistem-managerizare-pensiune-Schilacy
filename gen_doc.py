import os
import django
from pdoc import pdoc
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PensiuneaSchilacy.settings')

django.setup()

print("Generare documentatie...")

pdoc('cazare', output_directory=Path('./docs'))

print("Gata! Check 'docs'.")