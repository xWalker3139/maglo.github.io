from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

CATEGORIE_COPIL = (
    ('Carti','Carti'),
    ('Jucarii','Jucarii'),
    ('Haine','Haine'),
    ('Articole sportive','Articole sportive'),
    ('Schimburi', 'Schimburi'),
    ('Mama si copil', 'Mama si copil'),
)

CATEGORIE_ADULT = [
    ('Auto, moto si ambarcatiuni','Auto, moto si ambarcatiuni'),
    ('Piese auto', 'Piese auto'),
    ('Agro si industrie', 'Agro si industrie'),
    ('Imobiliare','Imobiliare'),
    ('Moda si frumusete','Moda si frumusete'),
    ('Electronice si electrocasnice', 'Electronice si electrocasnice'),
    ('Afaceri/Servicii', 'Afaceri/Servicii'),
    ('Animale de companie','Animale de companie'),
    ('Locuri de munca', 'Locuri de munca'),
    ('Sport, timp liber si Hobby', 'Sport, timp liber si Hobby'),
    ('Intreprinzatori autohtoni', 'Intreprinzatori autohtoni'),
    ('Matrimoniale', 'Matrimoniale'),
]

SUBCATEGORIE_ADULT = [
    ('Autoturisme', 'Ambarcatiuni', 'Autoutilitare', 'Camioane, rulote, remorci', 'Motociclete, scutere, ATV'),
    ('Roti, jante, anvelope', 'Caroserie', 'Mecanica electrica'),
    ('Utilaje agricole si industriale', 'Animale domestice', 'Produse piata'),
    ('Apartamente de vanzare', 'Apartamente de inchiriat', 'Birouri', 'Case/Vile de vanzare', 'Case/Vile de inchiriat', 'Terenuri agricole', 'Terenuri constructii', 'Spatii comerciale', 'Spatii industriale'),
    ('Haine dama', 'Haine barbati', 'Incaltaminte dama', 'Incaltaminte barbati', 'Bijuterii', 'Cosmetice', 'Accesorii'),
    ('Telefoane', 'Tablete', 'Electrocasnice', 'Laptop - Calculator', 'Aparate foto - Camere video', 'Console'),
    ('Cafenele', 'Cofetarii', 'Constructii', 'Cabinete medicale', 'Fast-Food-uri', 'Restaurante', 'Contabilitate', 'Digital Marketing', 'Grafic si Design', 'Meditatii', 'Programare si tehnologie', 'Video si animatii', 'Cabinet medical', 'Cabinet psihologic', 'Hotel', 'Pensiune'),
    ('Adoptii', 'Accesorii animale'),
    ('Agenti de vanzari', 'Confectii - Croitori', 'Cosmeticieni - Frizeri', 'Ingineri - Meseriasi - Constructori', 'Munca in strainatate', 'Paza si protectie', 'Personal hotelier-restaurant'),
    ('Articole sportive', 'Carti, Filme', 'Arta si antichitati', 'Muzica, instrumente muzicale'),
]

JUDETE = (
    ('Alba', 'Alba'),
    ('Arad', 'Arad'),
    ('Arges', 'Arges'),
    ('Bacau', 'Bacau'),
    ('Bihor', 'Bihor'),
    ('Bistrita-Nasaud', 'Bistrita-Nasaud'),
    ('Botosani', 'Botosani'),
    ('Braila', 'Braila'),
    ('Brasov', 'Brasov'),
    ('Buzau', 'Buzau'),
    ('Calarasi', 'Calarasi'),
    ('Caras-Severin', 'Caras-Severin'),
    ('Cluj', 'Cluj'),
    ('Constanta', 'Constanta'),
    ('Covasna', 'Covasna'),
    ('Dambovita', 'Dambovita'),
    ('Dolj', 'Dolj'),
    ('Galati', 'Galati'),
    ('Giurgiu', 'Giurgiu'),
    ('Gorj', 'Gorj'),
    ('Harghita', 'Harghita'),
    ('Hunedoara', 'Hunedoara'),
    ('Ialomita', 'Ialomita'),
    ('Iasi', 'Iasi'),
    ('Ilfov', 'Ilfov'),
    ('Maramures', 'Maramures'),
    ('Mehedinti', 'Mehedinti'),
    ('Mures', 'Mures'),
    ('Neamt', 'Neamt'),
    ('Olt', 'Olt'),
    ('Prahova', 'Prahova'),
    ('Salaj', 'Salaj'),
    ('Satu Mare', 'Satu Mare'),
    ('Sibiu', 'Sibiu'),
    ('Suceava', 'Suceava'),
    ('Teleorman', 'Teleorman'),
    ('Timis', 'Timis'),
    ('Tulcea', 'Tulcea'),
    ('Valcea', 'Valcea'),
    ('Vaslui', 'Vaslui'),
    ('Vrancea', 'Vrancea'),
)

SEARCHBAR_COPIL = (
    (JUDETE, JUDETE),
    (CATEGORIE_COPIL, CATEGORIE_COPIL),
)

TIPUL_AFACERII = (
    ('Cabinet medical', 'Cabinet medical'),
    ('Cabinet psihologic', 'Cabinet psihologic'),
    ('Cafenea', 'Cafenea'),
    ('Cofetarie', 'Cofetarie'),
    ('Constructii', 'Constructii'),
    ('Frizerii', 'Frizerii'),
    ('Hotel', 'Hotel'),
    ('Fast-Food-uri', 'Fast-Food-uri'),
    ('Pensiune', 'Pensiune'),
    ('Restaurant', 'Restaurant'),
    ('Saloane de coafura', 'Saloane de coafura'),
    ('Service Auto', 'Service Auto'),
)

TIPUL_SERVICIULUI = (
    ('Contabilitate', 'Contabilitate'),
    ('Consultanta', 'Consultanta'),
    ('Digital Marketing', 'Digital Marketing'),
    ('Grafic si Design', 'Grafic si Design'),
    ('Meditatii', 'Meditatii'),
    ('Programare si tehnologie', 'Programare si tehnologie'),
    ('Video si animatii', 'Video si animatii'),
)

class AjutorSiContact(models.Model):
    nume = models.CharField(max_length=264)
    email = models.EmailField()
    descriere = models.TextField(max_length=9000)

    def __str__(self):
        return self.nume

class Adult(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nume = models.CharField(max_length=264, null=True)
    emailul = models.EmailField(null=True)
    parola = models.CharField(max_length=264, null=True)

    def __str__(self):
        return self.nume

class Copil(models.Model):
    nume = models.CharField(max_length=264, null=True)
    prenume = models.CharField(max_length=264, null=True)
    email = models.EmailField(null=True)
    parola = models.CharField(max_length=264, null=True)

    def __str__(self):
        return self.nume

class AnuntCopil(models.Model):
    titlul = models.CharField(max_length=264, null=True, blank=True)
    numele_anuntului = models.CharField(max_length=264, null=True)
    descriere = models.TextField(max_length=9000)
    categorie_copil = models.CharField(max_length=264, choices=CATEGORIE_COPIL)
    telefon = models.PositiveIntegerField()
    email = models.EmailField()
    pret = models.FloatField(null=True, blank=True)
    moneda = models.CharField(max_length=264,null=True, blank=True)
    imagine = models.ImageField(null=True, blank=True, upload_to="images/")
    imagine2 = models.ImageField(null=True, blank=True, upload_to="images/")
    imagine3 = models.ImageField(null=True, blank=True, upload_to="images/")
    imagine4 = models.ImageField(null=True, blank=True, upload_to="images/")
    imagine5 = models.ImageField(null=True, blank=True, upload_to="images/")
    imagine6 = models.ImageField(null=True, blank=True, upload_to="images/")
    localizare = models.CharField(max_length=264, choices=JUDETE)

    def __str__(self):
        return self.descriere
    

class AnuntAdult(models.Model):
    titlul = models.CharField(max_length=264, null=True)
    descriere = models.TextField(max_length=9000)
    numele_anuntului = models.CharField(max_length=264, null=True)
    categorie_adult = models.CharField(max_length=264, null=True, blank=False)
    telefon = models.IntegerField()
    email = models.EmailField()
    pret = models.CharField(max_length=264, null=True, blank=False, default=1)
    moneda = models.CharField(max_length=264, null=True)
    imagine = models.ImageField(null=False, blank=False, upload_to='images/')
    imagine2 = models.ImageField(null=True, blank=False, upload_to='images/')
    imagine3 = models.ImageField(null=True, blank=False, upload_to='images/')
    imagine4 = models.ImageField(null=True, blank=False, upload_to='images/')
    imagine5 = models.ImageField(null=True, blank=False, upload_to='images/')
    imagine6 = models.ImageField(null=True, blank=False, upload_to='images/')
    subcategorie_adult = models.CharField(max_length=264, null=True)
    favorit = models.ManyToManyField(User, related_name="favorit", blank=True)
    localizare = models.CharField(max_length=264, choices=JUDETE)
    #########Autoturisme#######
    caroserie = models.Field(max_length=264, null=True, unique=True)
    capacitate_motor = models.CharField(max_length=264, null=True)
    combustibil = models.CharField(max_length=264, null=True)
    culoare = models.CharField(max_length=264, null=True)
    cutie_de_viteze = models.CharField(max_length=264, null=True)
    marca = models.CharField(max_length=264, null=True)
    rulaj = models.CharField(max_length=264, null=True)
    stare = models.CharField(max_length=264, null=True)
    ##########Imobiliare########
    numar_de_camere = models.CharField(max_length=264, null=True)
    compartimentare = models.CharField(max_length=264, null=True)
    suprafata_utila = models.CharField(max_length=264, null=True)
    an_de_constructie = models.CharField(max_length=264, null=True)
    etaj = models.CharField(max_length=264, null=True)
    teren = models.CharField(max_length=264, null=True)
    ###########Moda##############
    marime = models.CharField(max_length=264, null=True)
    ###########Locuri############
    tip_job = models.CharField(max_length=264, null=True)
    tip_contract = models.CharField(max_length=264, null=True)
    nivelul_de_studii = models.CharField(max_length=264, null=True)
    nivelul_de_experienta = models.CharField(max_length=264, null=True)
    mobilitatea_postului = models.CharField(max_length=264, null=True)
    program_flexibil = models.CharField(max_length=264, null=True)

    def __str__(self):
        return self.numele_anuntului

    def get_absolute_url(self):
        return reverse('my_app:anunturi_postate_adult', kwargs={'pk':self.pk})

class MesajCopil(models.Model):
    mesaj = models.TextField(max_length=9000)

    def __str__(self):
        return self.mesaj

class MesajAdult(models.Model):
    mesaj = models.TextField(max_length=9000)

    def __str__(self):
        return self.mesaj

class SearchBarCopil(models.Model):
    search = models.CharField(max_length=264, null=True)

    def __str__(self):
        return self.search

class Afacere(models.Model):
    titlul = models.CharField(max_length=264, null=True)
    numele_firmei = models.CharField(max_length=264, null=True)
    descriere = models.TextField(max_length=9000, null=True)
    imagine = models.ImageField(null=True, blank=True, upload_to='images/')
    imagine2 = models.ImageField(unique=True, null=True, blank=True, upload_to='images/')
    imagine3 = models.ImageField(unique=True, null=True, blank=True, upload_to='images/')
    imagine4 = models.ImageField(unique=True, null=True, blank=True, upload_to='images/')
    imagine5 = models.ImageField(unique=True, null=True, blank=True, upload_to='images/')
    imagine6 = models.ImageField(unique=True, null=True, blank=True, upload_to='images/')
    judet = models.CharField(max_length=264, choices=JUDETE)
    adresa = models.CharField(max_length=264, null=True)
    email = models.EmailField(null=True, blank=True)
    telefon = models.IntegerField(null=True, blank=True)
    tipul_afacerii = models.CharField(max_length=264, choices=TIPUL_AFACERII)

    def __str__(self):
        return self.descriere

class Serviciu(models.Model):
    titlul = models.CharField(max_length=264, null=True)
    numele_serviciului = models.CharField(max_length=264, null=True)
    descriere = models.TextField(max_length=9000, null=True)
    imagine = models.ImageField(unique=True, null=True, blank=True, upload_to='images/')
    imagine2 = models.ImageField(unique=True, null=True, blank=True, upload_to='images/')
    imagine3 = models.ImageField(unique=True, null=True, blank=True, upload_to='images/')
    imagine4 = models.ImageField(unique=True, null=True, blank=True, upload_to='images/')
    imagine5 = models.ImageField(unique=True, null=True, blank=True, upload_to='images/')
    imagine6 = models.ImageField(unique=True, null=True, blank=True, upload_to='images/')
    judet = models.CharField(max_length=264, choices=JUDETE)
    tipul_serviciului = models.CharField(max_length=264, choices=TIPUL_SERVICIULUI)
    email = models.EmailField(null=True, blank=True)
    experienta_profesionala = models.TextField(max_length=9000, null=True)
    telefon = models.IntegerField(null=True)

    def __str__(self):
        return self.numele_serviciului

class MesajAfaceri(models.Model):
    nume = models.CharField(max_length=264, null=True)
    email = models.EmailField(null=True)
    mesaj = models.TextField(max_length=9000, null=True)

    def __str__(self):
        return self.nume

class MesajServiciu(models.Model):
    nume = models.CharField(max_length=264, null=True)
    email = models.EmailField(null=True)
    mesaj = models.TextField(max_length=9000, null=True)

    def __str__(self):
        return self.nume

# Create your models here.
