from django.shortcuts import render, redirect,get_object_or_404 # <-- Am adaugat redirect
from .models import TipCamera,Rezervare,Camera,Factura
from .forms import RezervareForm # <-- Am importat formularul creat la pasul 1
from django.utils import timezone

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

def efectueaza_check_out(request, rezervare_id):
    # 1. Luam rezervarea
    rezervare = get_object_or_404(Rezervare, id=rezervare_id)
    
    # 2. Calculam numarul de nopti
    # Scadem datele si luam componenta ".days"
    durata = (rezervare.data_check_out - rezervare.data_check_in).days
    
    # Daca a stat 0 zile (a venit si a plecat azi), taxam totusi o noapte
    if durata == 0:
        durata = 1
        
    # 3. Calculam pretul total pe noapte (poate avea mai multe camere)
    pret_total_per_noapte = 0
    for camera in rezervare.camere.all():
        pret_total_per_noapte += camera.tip_camera.pret_per_noapte
        
        # 4. Eliberam camerele (le punem pe 'curatenie' sau 'libera')
        camera.stare = 'libera'
        camera.save()
        
    total_de_plata = pret_total_per_noapte * durata
    
    # 5. Generam Factura
    # Verificam daca nu cumva exista deja (ca sa nu o cream de doua ori)
    if not hasattr(rezervare, 'factura'):
        Factura.objects.create(
            rezervare=rezervare,
            numar_factura=f"F-{rezervare.id}-{timezone.now().strftime('%Y%m%d')}", # Ex: F-15-20231126
            total_plata=total_de_plata,
            este_platita=False # Receptionerul o va marca platita ulterior
        )
    
    # 6. Finalizam rezervarea
    rezervare.status = 'finalizata'
    rezervare.save()
    
    return redirect('lista_rezervari')