from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

"""
Modulul Models pentru Aplicația de Gestiune Hotelieră.

Acest modul definește structura bazei de date (ORM) pentru Pensiunea Schilacy.
Include definițiile pentru utilizatori cum ar fi personalul pensiunii, clienți, camere, rezervări
și sistemul de facturare.

Modele incluse:
    - Utilizator: Extinde userul standard Django cu roluri specifice.
    - Client: Datele de contact ale persoanelor care efectueaza cazarile.
    - Camera & TipCamera: Gestiunea camerelor și tipurilor de camere.
    - Rezervare: Check-in si Check-out.
    - Factura: Document emis automat.
    - Problema: Sistem de ticketing pentru eventualele probleme ale pensiunii.
"""

# 1. UTILIZATOR (Manager & Receptioner)
class Utilizator(AbstractUser):
    """
    Model pentru utilizatorii sistemului (personalul pensiunii).
    
    Extinde clasa AbstractUser din Django pentru a adăuga roluri specifice
    de acces.

    Attributes:
        rol (str): Rolul utilizatorului în sistem. 
                   Poate fi 'manager' (acces total) sau 'receptioner' (acces operațional).
    """
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('receptioner', 'Recepționer'),
    )
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default='receptioner')
    
    def este_manager(self):
        return self.rol == 'manager'
        
    def este_receptioner(self):
        return self.rol == 'receptioner'

# 2. CLIENT
class Client(models.Model):
    """
    Stocheaza datele de identificare și contact ale oaspeților.
    
    Acest model este folosit pentru a ține istoricul clienților și pentru
    a completa automat datele pe factură.

    Attributes:
        nume (str): Numele de familie.
        prenume (str): Prenumele clientului.
        email (str): Adresa de email (trebuie să fie unica).
        telefon (str): Numărul de telefon pentru contact rapid.
    """
    nume = models.CharField(max_length=50)
    prenume = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefon = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.nume} {self.prenume}"

# 3. TIP CAMERA
class TipCamera(models.Model):
    """
    Lista pentru tipurile de camere disponibile și prețurile lor.
    
    Permite modificarea centralizată a prețurilor. Dacă prețul pentru 
    'Camera Dublă' se schimbă aici, se va reflecta la toate camerele de acest tip.

    Attributes:
        nume_tip (str): Denumirea comercială (ex: 'Single', 'Matrimonială Deluxe').
        descriere (str): Detalii despre dotări și spațiu.
        facilitati (str): Listă de facilități (ex: 'TV, AC, Balcon').
        pret_per_noapte (Decimal): Tariful standard per noapte în RON.
    """
    nume_tip = models.CharField(max_length=50)
    descriere = models.TextField()
    facilitati = models.TextField(blank=True)
    pret_per_noapte = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nume_tip} - {self.pret_per_noapte} RON"

# 4. CAMERA
class Camera(models.Model):
    """
    Reprezintă o cameră fizică din pensiune.

    Attributes:
        numar_camera (str): Identificatorul unic al camerei (ex: '101').
        etaj (int): Etajul unde este situată (util pentru repartizare).
        stare (str): Statusul curent ('libera', 'ocupata', 'curatenie').
        tip_camera (ForeignKey): Legătura către definiția tipului (preț/facilități).
    """
    STATUS_CHOICES = (
        ('libera', 'Liberă'),
        ('ocupata', 'Ocupată'),
        ('curatenie', 'Curățenie'),
    )
    
    numar_camera = models.CharField(max_length=10, unique=True)
    etaj = models.IntegerField()
    stare = models.CharField(max_length=20, choices=STATUS_CHOICES, default='libera')
    tip_camera = models.ForeignKey(TipCamera, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.numar_camera} ({self.tip_camera.nume_tip}) - Etaj {self.etaj}"

# 5. REZERVARE
class Rezervare(models.Model):
    """
    Gestionează o rezervare creata de catre un client.
    
    Este entitatea centrală care leagă Clientul de Camere pentru o anumita perioadă de timp.

    Attributes:
        client (ForeignKey): Clientul rezervării.
        camere (ManyToManyField): Lista camerelor rezervate (permite rezervarea mai multor camere pe același nume).
        data_check_in (date): Data de început a rezervarii.
        data_check_out (date): Data de sfârșit a rezervarii.
        status (str): Starea rezervării ('activa' - curentă, 'anulata', 'finalizata' - după check-out).
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    camere = models.ManyToManyField(Camera)
    
    data_check_in = models.DateField()
    data_check_out = models.DateField()
    status = models.CharField(max_length=20, default='activa')
    
    def __str__(self):
        return f"Rezervare {self.id} - {self.client}"

# 6. FACTURA
class Factura(models.Model):
    """
    Document financiar emis automat la finalizarea rezervării.

    Attributes:
        rezervare (OneToOneField): Rezervarea pentru care s-a emis factura.
        numar_factura (str): Serie unică generată automat (Format: F-{ID}-{DATA}).
        data_emitere (datetime): Momentul generării (de obicei la Check-Out).
        total_plata (Decimal): Suma totală de plată calculată automat.
        este_platita (bool): Flag/Stare pentru a marca încasarea banilor.
    """
    rezervare = models.OneToOneField(Rezervare, on_delete=models.CASCADE)
    numar_factura = models.CharField(max_length=20, unique=True)
    data_emitere = models.DateTimeField(default=timezone.now)
    total_plata = models.DecimalField(max_digits=10, decimal_places=2)
    este_platita = models.BooleanField(default=False)

    def __str__(self):
        return f"Factura {self.numar_factura}"

# 7. PROBLEMĂ (TICKET)
class Problema(models.Model):
    """
    Sistem de ticketing pentru raportarea defecțiunilor tehnice.

    Attributes:
        titlu (str): Rezumatul scurt al problemei (ex: 'Bec ars camera 102').
        descriere (str): Detalii complete despre defecțiune.
        data_raportare (datetime): Data și ora înregistrării (automată).
        rezolvata (bool): Statusul problemei (False = Activă, True = Rezolvată).
        raportata_de (ForeignKey): Utilizatorul care a deschis tichetul.
    """
    titlu = models.CharField(max_length=100)
    descriere = models.TextField()
    data_raportare = models.DateTimeField(auto_now_add=True)
    rezolvata = models.BooleanField(default=False)
    raportata_de = models.ForeignKey(Utilizator, on_delete=models.CASCADE)

    def __str__(self):
        return self.titlu