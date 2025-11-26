from django.shortcuts import render
from .models import TipCamera  # <-- 1. Importam modelul (tabela)

def homepage(request):
    # 2. Interogam baza de date: "Select * from TipCamera"
    toate_tipurile = TipCamera.objects.all()
    
    # 3. Impachetam datele intr-un dictionar numit "context"
    context = {
        'tipuri': toate_tipurile
    }
    
    # 4. Trimitem datele catre HTML
    return render(request, 'cazare/homepage.html', context)