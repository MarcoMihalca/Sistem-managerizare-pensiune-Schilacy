from django.shortcuts import render, redirect,get_object_or_404 # <-- Am adaugat redirect
from .models import TipCamera,Rezervare,Camera,Factura,Utilizator,Problema
from .forms import RezervareForm , ProblemaForm # <-- Am importat formularul creat la pasul 1
from django.utils import timezone
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required # <-- Adauga asta sus de tot
from django.contrib import messages

"""
Modulul Views (Logica de Business).

Acest modul gestionează cererile HTTP primite de la utilizator, procesează datele
și returnează răspunsurile corespunzătoare (pagini HTML).

Responsabilități principale:
- Gestionarea fluxului de rezervări (creare, listare, anulare).
- Implementarea logicii de Check-Out (calcul costuri, emitere facturi).
- Securizarea accesului (decoratorul @login_required).
- Generarea rapoartelor manageriale (statistici).
- Sistemul de ticketing pentru probleme tehnice.
"""

@login_required
def homepage(request):
    """
    Afișează pagina principală (Dashboard-ul aplicației).

    Interoghează baza de date pentru a prelua tipurile de camere disponibile
    și le trimite către șablonul HTML pentru a fi afișate în oferta publică.
    Accesul este permis doar utilizatorilor autentificați.

    Args:
        request (HttpRequest): Obiectul cererii HTTP.

    Returns:
        HttpResponse: Pagina 'homepage.html' randată cu contextul datelor.
    """
    toate_tipurile = TipCamera.objects.all()
    context = {'tipuri': toate_tipurile}
    return render(request, 'cazare/homepage.html', context)

# --- Functia Noua ---
@login_required
@login_required
def creare_rezervare(request):
    if request.method == 'POST':
        form = RezervareForm(request.POST)
        if form.is_valid():
            # 1. Extragem datele din formular (fara sa salvam inca)
            rezervare_noua = form.save(commit=False)
            
            check_in = form.cleaned_data['data_check_in']
            check_out = form.cleaned_data['data_check_out']
            camere_selectate = form.cleaned_data['camere'] # Lista de camere bifate

            # Validare simpla: Check-out sa nu fie inainte de Check-in
            if check_out <= check_in:
                messages.error(request, "Eroare: Data de Check-Out trebuie să fie după Check-In!")
                return render(request, 'cazare/creare_rezervare.html', {'form': form})

            # 2. VERIFICAREA DE SUPRAPUNERE (Partea cruciala)
            conflict = False
            mesaj_eroare = ""

            for camera in camere_selectate:
                # Cautam rezervari ACTIVE care se suprapun
                # Excludem rezervarile anulate sau finalizate
                suprapuneri = Rezervare.objects.filter(
                    camere=camera,
                    status='activa', # Verificam doar rezervarile active
                    data_check_in__lt=check_out, # Inceput vechi < Sfarsit nou
                    data_check_out__gt=check_in  # Sfarsit vechi > Inceput nou
                )

                if suprapuneri.exists():
                    conflict = True
                    # Luam prima rezervare care incurca ca sa spunem cine e
                    rez_existenta = suprapuneri.first()
                    mesaj_eroare = f"Camera {camera} este deja ocupată în perioada aleasă! (Rezervare ID: {rez_existenta.id})"
                    break # Ne oprim la prima eroare gasita

            if conflict:
                # Daca e conflict, NU salvam. Dam eroare pe ecran.
                messages.error(request, mesaj_eroare)
                # Trimitem formularul inapoi ca sa mai incerce o data
                return render(request, 'cazare/creare_rezervare.html', {'form': form})
            
            # 3. Daca nu e niciun conflict, salvam totul
            rezervare_noua.save()
            form.save_m2m() # Salvam relatia Many-to-Many cu camerele
            
            # Actualizam starea camerelor vizual (optional, pentru ca acum avem verificarea logica)
            for camera in camere_selectate:
                camera.stare = 'ocupata'
                camera.save()

            messages.success(request, "Rezervarea a fost creată cu succes!")
            return redirect('lista_rezervari')
    else:
        form = RezervareForm()
    
    return render(request, 'cazare/creare_rezervare.html', {'form': form})
@login_required
def lista_rezervari(request):
    """
    Afișează registrul tuturor rezervărilor din sistem.

    Datele sunt sortate descrescător după data de check-in (cele mai noi primele)
    pentru a oferi recepționerului o vedere rapidă asupra sosirilor recente.

    Context Template:
        rezervari: QuerySet cu toate obiectele Rezervare.
    """
    # Luam toate rezervarile, ordonate dupa data (cele mai recente primele)
    rezervari = Rezervare.objects.all().order_by('-data_check_in')
    
    context = {
        'rezervari': rezervari
    }
    return render(request, 'cazare/lista_rezervari.html', context)

@login_required
def anuleaza_rezervare(request, rezervare_id):
    """
    Marchează o rezervare ca fiind anulată.

    Nu șterge rezervarea din baza de date, ci doar îi schimbă
    statusul în 'anulata' pentru a păstra istoricul.

    Args:
        rezervare_id (int): ID-ul rezervării țintă.
    """
    # 1. Cautam rezervarea dupa ID
    rezervare = get_object_or_404(Rezervare, id=rezervare_id)
    
    # 2. Modificam statusul
    rezervare.status = 'anulata'
    rezervare.save()
    
    # 3. Ne intoarcem la lista
    return redirect('lista_rezervari')

@login_required
def efectueaza_check_out(request, rezervare_id):
    """
    Execută logica de finalizare a unei rezervari (Check-Out).

    Pași procesați automat:
    1. Calculează durata șederii (CheckOut - CheckIn).
            - Dacă durata este 0 zile, se taxează minim o noapte.
    2. Iterează prin toate camerele rezervării pentru a calcula prețul total
       (Preț cameră * Nr. nopti).
    3. Eliberează camerele (le schimbă starea din 'ocupata' în 'libera').
    4. Generează automat o Factură Fiscală unică asociată rezervării.
    5. Actualizează statusul rezervării în 'finalizata'.

    Args:
        rezervare_id (int): ID-ul rezervării care se finalizează.
    """
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

@login_required
def vizualizare_factura(request, factura_id):
    """
    Afișează detaliile unei facturi emise.

    Pagina HTML rezultată este optimizată pentru tipărire,
    ascunzând elementele de navigare pe foaia fizică.
    """
    factura = get_object_or_404(Factura, id=factura_id)
    return render(request, 'cazare/factura.html', {'factura': factura})

@login_required
def rapoarte_manager(request):
    """
    Generează dashboard-ul statistic pentru manageri.

    Conecteaza si culege datele în timp real folosind funcții SQL (SUM, COUNT)
    prin intermediul Django ORM:
    - Venituri Totale: Suma tuturor facturilor emise.
    - Statistici Operaționale: Numărul total de rezervări, anulări și finalizări.

    Securitate:
        Verifică explicit dacă utilizatorul are rolul de 'manager'.
        În caz contrar, redirecționează către pagina principală.
    """
    # 1. Calculam Veniturile Totale (Suma tuturor facturilor emise)
    # Folosim functia 'aggregate' care returneaza un dictionar
    if not request.user.este_manager():
         return redirect('acasa')
    situatie_financiara = Factura.objects.aggregate(total_incasari=Sum('total_plata'))
    
    # Daca nu exista nicio factura, rezultatul e None, asa ca punem 0
    venit_total = situatie_financiara['total_incasari'] or 0

    # 2. Numarul total de rezervari
    total_rezervari = Rezervare.objects.count()

    # 3. Numarul de rezervari finalizate vs anulate (Statistica)
    rezervari_finalizate = Rezervare.objects.filter(status='finalizata').count()
    rezervari_anulate = Rezervare.objects.filter(status='anulata').count()

    # 4. (Optional) Cea mai populara camera (Query complex)
    # Numaram de cate ori apare fiecare camera in rezervari
    
    context = {
        'venit_total': venit_total,
        'total_rezervari': total_rezervari,
        'rezervari_finalizate': rezervari_finalizate,
        'rezervari_anulate': rezervari_anulate,
    }
    
    return render(request, 'cazare/rapoarte.html', context)

from .models import Utilizator, Problema # Asigura-te ca sunt importate
from .forms import RezervareForm, ProblemaForm # Importa si noul formular

# --- SECTIUNEA TICKETING ---

@login_required
def raporteaza_problema(request):
    """
    Gestionează formularul de raportare a defecțiunilor tehnice.

    La salvarea form-ului, atașează automat problema utilizatorului curent
    (sau primului utilizator din bază, în versiunea curentă de test)
    pentru a asigura trasabilitatea sesizării.
    """
    if request.method == 'POST':
        form = ProblemaForm(request.POST)
        if form.is_valid():
            problema = form.save(commit=False)
            # TRUC TEMPORAR: Pentru ca nu avem Login, atribuim problema primului user din baza de date (Adminul)
            # Cand vom baga login, vom schimba cu: problema.raportata_de = request.user
            problema.raportata_de = Utilizator.objects.first() 
            problema.save()
            return redirect('acasa') # Dupa ce raporteaza, il trimitem acasa
    else:
        form = ProblemaForm()
    
    return render(request, 'cazare/raporteaza_problema.html', {'form': form})

@login_required
def lista_probleme(request):
    """
    Afișează tabloul de bord pentru mentenanță.

    Separă problemele în două liste distincte:
    1. Active: Probleme nerezolvate, care necesită atenție imediată.
    2. Istoric: Probleme marcate deja ca rezolvate.
    """
    # Luam doar problemele nerezolvate (active)
    probleme_active = Problema.objects.filter(rezolvata=False).order_by('-data_raportare')
    # Luam si istoricul celor rezolvate (optional)
    probleme_vechi = Problema.objects.filter(rezolvata=True).order_by('-data_raportare')
    
    context = {
        'active': probleme_active,
        'vechi': probleme_vechi
    }
    return render(request, 'cazare/lista_probleme.html', context)

@login_required
def rezolva_problema(request, problema_id):
    """
    Închide un tichet de suport tehnic.

    Setează flag-ul 'rezolvata' pe True, mutând problema din lista activă
    în istoric.

    Args:
        problema_id (int): ID-ul problemei rezolvate.
    """
    problema = get_object_or_404(Problema, id=problema_id)
    problema.rezolvata = True
    problema.save()
    return redirect('lista_probleme')