from django.shortcuts import render, redirect  # <-- Am adaugat redirect
from .models import TipCamera
from .forms import RezervareForm # <-- Am importat formularul creat la pasul 1

def homepage(request):
    toate_tipurile = TipCamera.objects.all()
    context = {'tipuri': toate_tipurile}
    return render(request, 'cazare/homepage.html', context)

# --- Functia Noua ---
def creare_rezervare(request):
    if request.method == 'POST':
        # Daca userul a apasat butonul "Salveaza"
        form = RezervareForm(request.POST)
        if form.is_valid():
            form.save()  # Salvam in baza de date
            return redirect('acasa')  # Il trimitem inapoi la prima pagina
    else:
        # Daca userul doar a intrat pe pagina
        form = RezervareForm()

    return render(request, 'cazare/creare_rezervare.html', {'form': form})