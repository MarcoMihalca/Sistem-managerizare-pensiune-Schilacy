from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# 1. UTILIZATOR (Manager & Receptioner)
class Utilizator(AbstractUser):
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
    nume = models.CharField(max_length=50)
    prenume = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telefon = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.nume} {self.prenume}"

# 3. TIP CAMERA
class TipCamera(models.Model):
    nume_tip = models.CharField(max_length=50)
    descriere = models.TextField()
    facilitati = models.TextField(blank=True)
    pret_per_noapte = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nume_tip} - {self.pret_per_noapte} RON"

# 4. CAMERA
class Camera(models.Model):
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
        return f"Camera {self.numar_camera} ({self.stare})"

# 5. REZERVARE
class Rezervare(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    camere = models.ManyToManyField(Camera)
    
    data_check_in = models.DateField()
    data_check_out = models.DateField()
    status = models.CharField(max_length=20, default='activa')
    
    def __str__(self):
        return f"Rezervare {self.id} - {self.client}"

# 6. FACTURA
class Factura(models.Model):
    rezervare = models.OneToOneField(Rezervare, on_delete=models.CASCADE)
    numar_factura = models.CharField(max_length=20, unique=True)
    data_emitere = models.DateTimeField(default=timezone.now)
    total_plata = models.DecimalField(max_digits=10, decimal_places=2)
    este_platita = models.BooleanField(default=False)

    def __str__(self):
        return f"Factura {self.numar_factura}"

# 7. PROBLEMĂ (TICKET)
class Problema(models.Model):
    titlu = models.CharField(max_length=100)
    descriere = models.TextField()
    data_raportare = models.DateTimeField(auto_now_add=True)
    rezolvata = models.BooleanField(default=False)
    raportata_de = models.ForeignKey(Utilizator, on_delete=models.CASCADE)

    def __str__(self):
        return self.titlu