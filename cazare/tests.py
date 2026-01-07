from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import TipCamera, Camera, Rezervare, Client
from datetime import date, timedelta

# Luam modelul nostru de utilizator personalizat
User = get_user_model()

class TestPensiune(TestCase):
    
    # setUp este o functie speciala care ruleaza INAINTE de fiecare test
    # Aici pregatim terenul (cream date false de test)
    def setUp(self):
        # 1. Cream un user Manager ca sa ne putem loga
        self.manager = User.objects.create_user(
            username='manager_test', 
            password='parola_test', 
            rol='manager'
        )
        
        # 2. Cream un Tip de Camera (Ex: Standard - 100 RON)
        self.tip_standard = TipCamera.objects.create(
            nume_tip="Camera Standard",
            pret_per_noapte=100,
            descriere="Test",
            facilitati="Wifi"
        )
        
        # 3. Cream o Camera fizica
        self.camera_101 = Camera.objects.create(
            numar_camera="101",
            tip_camera=self.tip_standard,
            stare='libera' ,
            etaj=1
        )
        
        # 4. Cream un Client
        self.client_ion = Client.objects.create(
            nume="Popescu",
            prenume="Ion",
            telefon="0700000000",
            email="ion@test.com"
        )

    # --- TESTUL 1: Verificam daca paginile merg (Homepage) ---
    def test_homepage_status(self):
        # Ne logam virtual
        self.client.login(username='manager_test', password='parola_test')
        
        # Incercam sa accesam pagina principala ('acasa' e numele din urls.py)
        response = self.client.get(reverse('acasa'))
        
        # Codul 200 inseamna "OK Success"
        self.assertEqual(response.status_code, 200)

    # --- TESTUL 2: Securitate (Cineva nelogat nu are voie la Rapoarte) ---
    def test_acces_rapoarte_nelogat(self):
        # Ne asiguram ca NU suntem logati
        self.client.logout()
        
        # Incercam sa intram la rapoarte
        response = self.client.get(reverse('rapoarte_manager'))
        
        # Ar trebui sa NU primim 200 (OK), ci 302 (Redirect catre Login)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

    # --- TESTUL 3: Logica de Business (Calcul matematic) ---
    def test_creare_rezervare_si_calcul(self):
        # Simulam o rezervare de 3 nopti
        data_in = date.today()
        data_out = data_in + timedelta(days=3) # 3 nopti
        
        rezervare = Rezervare.objects.create(
            client=self.client_ion,
            data_check_in=data_in,
            data_check_out=data_out,
            status='activa'
        )
        rezervare.camere.add(self.camera_101)
        
        # Verificam matematica:
        # 3 nopti * 100 RON (pretul camerei create in setUp) = 300 RON
        
        # Calculam durata
        durata = (rezervare.data_check_out - rezervare.data_check_in).days
        pret_total = durata * self.camera_101.tip_camera.pret_per_noapte
        
        # AssertEqual verifica daca (300 == 300)
        self.assertEqual(durata, 3)
        self.assertEqual(pret_total, 300)