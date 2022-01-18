from django import forms
from .models import Adult, Copil, AnuntAdult, AnuntCopil, AjutorSiContact, MesajCopil, MesajAdult, Afacere, Serviciu, MesajAfaceri, MesajServiciu
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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

class AdultForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nume', 'name':'username'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email', 'name':'email'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Parola', 'name':'password'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Parola', 'name':'password'}),
        }

class CopilForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numele'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Parola', 'name':'password'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Verifica-ti parola', 'name':'password'}),
        }

class AnuntCopilForm(forms.ModelForm):
    class Meta:
        model = AnuntCopil
        fields = '__all__'
        widgets = {
            'titlul':forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'Tilul'}),
            'descriere':forms.Textarea(attrs={'class':'form-control mb-2','placeholder':'Descriere'}),
            'email':forms.EmailInput(attrs={'class':'form-control mb-2','placeholder':'Email', 'name':'email2'}),
            'telefon':forms.NumberInput(attrs={'class':'form-control mb-2','placeholder':'Numar de telefon'}),
            'localizare':forms.Select(attrs={'class':'form-control mb-2','placeholder':'Localizare'}),
            'categorie_copil':forms.Select(attrs={'class':'form-control mb-2','placeholder':'Categoria'}),
            'pret':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Pret'}),
            'imagine':forms.FileInput(attrs={'id':'imagine'})
        }

class AnuntAdultForm(forms.ModelForm):
    class Meta:
        model = AnuntAdult
        fields = ('user', )
        widgets = {
            'user':forms.TextInput(attrs={'class':'form-control', 'id':'user1', 'value':'', 'type':'hidden'}),
        }

class AjutorSiContactForm(forms.ModelForm):
    class Meta:
        model = AjutorSiContact
        fields = '__all__'
        widgets = {
            'nume':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nume'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
            'descriere':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descriere'}),
        }

class MesajCopilForm(forms.ModelForm):
    class Meta:
        model = MesajCopil
        fields = '__all__'
        widgets = {
            'mesaj':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Trimite mesajul tau vanzatorului...', 'id':'mesaj', 'name':'mesaj'})
        }

class MesajAdultForm(forms.ModelForm):
    class Meta:
        model = MesajAdult
        fields = '__all__'
        widgets = {
            'mesaj':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Trimite mesajul tau vanzatorului...', 'id':'mesaj', 'name':'mesaj_adult'})
        }

class AfacereForm(forms.ModelForm):
    class Meta:
        model = Afacere
        fields = '__all__'
        widgets = {
            'titlul':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titlul afacerii'}),
            'descriere':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descrierea afacerii'}),
            'imagine':forms.FileInput(attrs={'id':'imagine'}),
            'judet':forms.Select(attrs={'class':'form-control'}),
            'adresa':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adresa'}),
            'tipul_afacerii':forms.Select(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
        }

class ServiciuForm(forms.ModelForm):
    class Meta:
        model = Serviciu
        fields = '__all__'
        widgets = {
            'titlul':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titlul serviciului'}),
            'descriere':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descrierea serviciului...'}),
            'imagine':forms.FileInput(attrs={'id':'imagine'}),
            'judet':forms.Select(attrs={'class':'form-control'}),
            'tipul_serviciului':forms.Select(attrs={'class':'form-control'}),
            'experienta_profesionala':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Experienta ta profesionala...'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'})
        }

class MesajAfaceriForm(forms.ModelForm):
    class Meta:
        model = MesajAfaceri
        fields = '__all__'
        widgets = {
            'nume':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nume', 'name':'nume5'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email', 'name':'email5'}),
            'mesaj':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Mesaj', 'name':'mesaj5'}),
        }

class MesajServiciuForm(forms.ModelForm):
    class Meta:
        model = MesajServiciu
        fields = '__all__'
        widgets = {
            'nume':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nume', 'name':'nume6'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email', 'name':'email6'}),
            'mesaj':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Mesaj', 'name':'mesaj6'}),
        }
