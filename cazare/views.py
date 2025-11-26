from django.shortcuts import render, redirect,get_object_or_404 # <-- Am adaugat redirect
from .models import TipCamera,Rezervare,Camera
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

def lista_rezervari(request):
    # Luam toate rezervarile, ordonate dupa data (cele mai recente primele)
    rezervari = Rezervare.objects.all().order_by('-data_check_in')
    
    context = {
        'rezervari': rezervari
    }
    return render(request, 'cazare/lista_rezervari.html', context)

def anuleaza_rezervare(request, rezervare_id):
    # 1. Cautam rezervarea dupa ID
    rezervare = get_object_or_404(Rezervare, id=rezervare_id)
    
    # 2. Modificam statusul
    rezervare.status = 'anulata'
    rezervare.save()
    
    # 3. Ne intoarcem la lista
    return redirect('lista_rezervari')