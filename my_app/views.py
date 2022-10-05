from django.shortcuts import get_object_or_404, render, redirect
from .models import TIPUL_AFACERII, Adult, Copil, AnuntAdult, AnuntCopil, AjutorSiContact, CATEGORIE_COPIL, MesajCopil, JUDETE, CATEGORIE_ADULT, SUBCATEGORIE_ADULT, Afacere, Serviciu, MesajAfaceri, MesajServiciu, Mesaj_Copil
from .forms import AdultForm, Adult_ReForm, Copil_ReForm, CopilForm, AnuntAdultForm, AnuntCopilForm, AjutorSiContactForm, MesajCopilForm, AfacereForm, ServiciuForm, MesajAfaceriForm, MesajServiciuForm
from django.views.generic import View
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .filters import SearchFilter
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from agora_token_builder import RtcTokenBuilder
from rest_framework.parsers import JSONParser
from .serializers import MessageSerializer
import datetime
import random
import json
import time

########################################
###############BAZA#####################
########################################


class BaseView(View):
    def get(self, request):
        date_posted = datetime.datetime.now().year
        model1 = AnuntAdult.objects.all()
        model2 = AnuntCopil.objects.all()
        model3 = Afacere.objects.all()
        model4 = Serviciu.objects.all()
        context = {
            'date_posted':date_posted,
            'model1':model1,
            'model2':model2,
            'model3':model3,
            'model4':model4,
            'range':range(0, 3),
        }
        if request.method == "POST":
            cautat = request.POST['cautat']
            lookup = (Q(localizare__icontains = cautat) and Q(categorie_adult__icontains = cautat))
            return render(request, "my_app/base.html", context)
        return render(request, "my_app/base.html", context)

class TermeniConditii(View):
    def get(self, request):
        date_posted = datetime.datetime.now().year
        return render(request, "my_app/termeni_si_conditii.html", {'date_posted':date_posted})

def AjutorSiContact(request):
    form = AjutorSiContactForm
    data_postarii = datetime.datetime.now().year
    if request.method == 'POST':
        form = AjutorSiContactForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return Http404
    else:
        return render(request, "my_app/ajutor_si_contact.html", {'form':form, 'data_postarii':data_postarii})
    return render(request, "my_app/ajutor_si_contact.html", {'form':form, 'data_postarii':data_postarii})

class PoliticaDeConfidentialitate(View):
    def get(self, request):
        date_posted = datetime.datetime.now().year
        return render(request, 'my_app/politica_confi.html', {'date_posted':date_posted}) 

class PoliticaDeCookieuri(View):
    def get(self, request):
        date_posted = datetime.datetime.now().year
        return render(request, "my_app/politica_cookie.html", {'date_posted':date_posted})

class Securitate(View):
    def get(self, request):
        date_posted = datetime.datetime.now().year
        return render(request, 'my_app/securitate.html', {'date_posted':date_posted})

#############################################
############COPIL############################
#############################################

###############CONTUL_MEU####################

@login_required
def contul_meu_copil(request):
    date_posted = datetime.datetime.now().year
    model = request.user.copil
    form = Copil_ReForm(instance=model)
    context = {
        'date_posted':date_posted,
        'model':model,
        'form':form,
    }
    return render(request, "my_app/contul_meu_copil.html", context)

@login_required
def actualizare_date_copil(request):
    date_posted = datetime.datetime.now().year
    model = request.user.copil
    form = Copil_ReForm(instance=model)
    if request.method == "POST":
        form = Copil_ReForm(request.POST, request.FILES, instance=model)
        if form.is_valid:
            form.save()
        else:
            form = Copil_ReForm()
    context = {
        'date_posted':date_posted,
        'model':model,
        'form':form,
    }
    return render(request, "my_app/actualizare_date_copil.html", context)

@login_required
def schimb_parola_copil(request, pk):
    model = User.objects.get(id=pk)
    form = CopilForm()
    date_posted = datetime.datetime.now().year
    if request.method == "POST":
        form = CopilForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_app/contul_meu_copil')
    return render(request, "my_app/schimb_parola_copil.html", {'model':model, 'form':form, 'date_posted':date_posted})

def pag_anunturi_postate(request, pk):
    model = AnuntCopil.objects.filter(id=pk)
    new_model = User.objects.filter(id=pk)
    my_model = MesajCopil.objects.all()
    date_posted = datetime.datetime.now().year
    form = CopilForm()
    new_form = MesajCopilForm()
    favorit_id = False
    anunt = AnuntCopil.objects.get(id=pk)
    if anunt.favorite.filter(id=request.user.id).exists():
        favorit_id = True
    if request.method == "POST":
        form = CopilForm(request.POST)
        if form.is_valid():
            form.save()
    if request.method == "POST":
        new_form = MesajCopilForm(request.POST)
        if new_form.is_valid():
            new_form.save()
    if request.method == "POST":
        email = request.POST.get('email')
        new_email = request.POST.get('email2')
        mesaj = request.POST.get('mesaj')
        send_mail(
            'Maglo',
            mesaj,
            email,
            new_email
        )
    return render(request, "my_app/pag_anunturi_postate.html", {'model':model, 'form':form, 'date_posted':date_posted, 'new_model':new_model,'my_model':my_model, 'new_form':new_form, 'anunt':anunt, 'favorit_id':favorit_id})

###############CRUD###########################

@login_required
def pag_update_copil(request):
    model = AnuntCopil.objects.all()
    date_posted = datetime.datetime.now().year
    return render(request, "my_app/pag_update_copil.html", {'model':model, 'date_posted':date_posted})

@login_required
def update_copil(request, pk):
    model = AnuntCopil.objects.get(id=pk)
    form = AnuntCopilForm(instance=model)
    date_posted = datetime.datetime.now().year
    if request.method == 'POST':
        form = AnuntCopilForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect('/my_app/pag_update_copil')
    context = {
        'model':model,
        'form':form,
        'date_posted':date_posted,
    }
    return render(request, 'my_app/update_copil.html', context)

@login_required
def pag_delete_copil(request):
    model = AnuntCopil.objects.all()
    date_posted = datetime.datetime.now().year
    return render(request, "my_app/pag_delete_copil.html", {'model':model, 'date_posted':date_posted})

@login_required
def delete_copil(request, pk):
    model = AnuntCopil.objects.get(id=pk)
    date_posted = datetime.datetime.now().year
    data_anunt = datetime.datetime.now()
    if request.method == "POST":
        model.delete()
        return redirect('/my_app/anunturi_totale_copil')
    context = {
        'model':model,
        'date_posted':date_posted,
        'data_anunt':data_anunt,
    }
    return render(request, 'my_app/delete_copil.html', context)

##############################################

@login_required
def anunturi_favorite_copil(request):
    date_posted = datetime.datetime.now().year
    user = request.user
    anunt_favorit = user.favorite.all()
    context = {
        'date_posted':date_posted,
        'anunt_favorit':anunt_favorit
    }
    return render(request, "my_app/anunturi_favorite_copil.html", context)

def adauga_anunturi_favorite_c(request, pk):
    anunt = get_object_or_404(AnuntCopil, id=request.POST.get('favorite'))
    favorit_id = False
    if anunt.favorite.filter(id=request.user.id).exists():
        anunt.favorite.remove(request.user)
        favorit_id = True
    else:
        anunt.favorite.add(request.user)
        favorit_id = False
    return HttpResponseRedirect(reverse("my_app:pag_anunturi_postate", args=[str(pk)]))

@login_required
def deconectare_copil1(request):
    date_posted = datetime.datetime.now().year
    return render(request, "my_app/deconectare_copil.html", {'date_posted':date_posted})

@login_required
def deconectare_copil(request):
    logout(request)
    return HttpResponseRedirect(reverse('anunturi_postate_copil'))

@login_required
def anunturi_totale_copil(request):
    model = AnuntCopil.objects.all()
    return render(request, "my_app/anunturi_totale_copil.html", {'model':model})

@login_required
def pag_anunturi_copil(request, pk):
    date_posted = datetime.datetime.now().year
    model = AnuntCopil.objects.get(id=pk)
    new_model = AnuntCopil.objects.all()
    context = {
        'date_posted':date_posted,
        'model':model,
        'new_model':new_model,
    }
    return render(request, 'my_app/pag_anunturi_copil.html', context)

def inregistrare_copil(request):
    date_posted = datetime.datetime.now().year
    form = CopilForm()
    if request.method == "POST":
        form = CopilForm(request.POST)
        if form.is_valid():
            user = form.save()
            Copil.objects.create(
                user=user,
                nume=user.username,
            )
            return redirect('my_app:autentificate_copil')
        else:
            messages.warning(request, "Parola este prea scurta! Pentru a va imbunatatii parola folositi minim 8 caractere, numere si semne de punctuatie!")
    return render(request, "my_app/inregistrare_copil.html", {'form':form, 'date_posted': date_posted})

def autentificate_copil(request):
    date_posted = datetime.datetime.now().year
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('my_app:contul_meu_copil')
        else:
            messages.warning(request, "Numele sau parola este incorecta!")
    return render(request, "my_app/autentificate_copil.html", {'date_posted':date_posted})

@login_required
def posteaza_anunt_copil(request):
    date_posted = datetime.datetime.now().year
    if request.method == "POST":
        titlul = request.POST.get("titlul")
        numele_anuntului = request.POST.get('numele_anuntului')
        descriere = request.POST.get("descriere")
        categorie_copil = request.POST.get("categorie_copil")
        telefon = request.POST.get("telefon")
        email = request.POST.get("email")
        pret = request.POST.get("pret")
        moneda = request.POST.get("moneda")
        imagine = request.FILES.get("imagine")
        imagine2 = request.FILES.get("imagine2")
        imagine3 = request.FILES.get("imagine3")
        imagine4 = request.FILES.get("imagine4")
        imagine5 = request.FILES.get("imagine5")
        imagine6 = request.FILES.get("imagine6")
        localizare = request.POST.get("localizare")
        model = AnuntCopil(titlul=titlul,numele_anuntului=numele_anuntului, descriere=descriere, categorie_copil=categorie_copil, telefon=telefon, email=email, pret=pret, imagine=imagine, localizare=localizare, moneda=moneda, 
                            imagine2=imagine2, imagine3=imagine3, imagine4=imagine4, imagine5=imagine5, imagine6=imagine6)
        model.save()
    context = {
        'date_posted':date_posted,
    }
    return render(request, "my_app/posteaza_anunt_copil.html", context)

################################################
######################CHAT######################
################################################

@login_required
def cautare_user(request):
    date_posted = datetime.datetime.now().year
    if request.method == "POST":
        name = request.POST.get("name")
        lookup = (Q(username__icontains = name))
        model = User.objects.filter(lookup)
        return render(request, "my_app/cautare_user.html", {'date_posted':date_posted, 'model':model})
    else:
        return render(request, "my_app/cautare_user.html", {'date_posted':date_posted})

@login_required
def video_room(request):
    date_posted = datetime.datetime.now().year
    context = {
        'date_posted':date_posted,
    }
    return render(request, "my_app/video_room.html", context)

@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Mesaj_Copil.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def chat_view(request):
    date_posted = datetime.datetime.now().year
    if not request.user.is_authenticated:
        return redirect('my_app/base')
    if request.method == "GET":
        return render(request, 'my_app/chat_copil.html',
                      {'users': User.objects.exclude(username=request.user.username), 'date_posted':date_posted})


def message_view(request, sender, receiver):
    date_posted = datetime.datetime.now().year
    if not request.user.is_authenticated:
        return redirect('my_app/base')
    if request.method == "GET":
        return render(request, "my_app/mesaj_copil.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Mesaj_Copil.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Mesaj_Copil.objects.filter(sender_id=receiver, receiver_id=sender),
                        'date_posted':date_posted})

#################CATEGORII#######################

def carti_copil(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_COPIL[0][1]
    model = AnuntCopil.objects.filter(categorie_copil=categorie)
    return render(request, "my_app/carti_copil.html", {'date_posted':date_posted, 'model':model})

def pag_carti_copil(request, pk):
    date_posted = datetime.datetime.now().year
    model = AnuntCopil.objects.get(id=pk)
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/pag_carti_copil.html', context)

def jucarii_copil(request):
    categorie = CATEGORIE_COPIL[1][1]
    model = AnuntCopil.objects.filter(categorie_copil=categorie)
    date_posted = datetime.datetime.now().year
    return render(request, "my_app/jucarii_copil.html", {'date_posted':date_posted, 'model':model})

def pag_jucarii_copil(request, pk):
    date_posted = datetime.datetime.now().year
    model = AnuntCopil.objects.get(id=pk)
    context = {
        'model':model,
        'date_posted':date_posted,
    }
    return render(request, 'my_app/pag_jucarii_copil.html', context)

def haine_copil(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_COPIL[2][1]
    model = AnuntCopil.objects.filter(categorie_copil = categorie)
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/haine_copii.html", context)

def pag_haine_copil(request, pk):
    date_posted = datetime.datetime.now().year
    model = AnuntCopil.objects.get(id=pk)
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/pag_haine_copil.html', context)

def articole_sportive_copil(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_COPIL[3][1]
    model = AnuntCopil.objects.filter(categorie_copil = categorie)
    return render(request, "my_app/articole_sportive_copil.html", {'date_posted':date_posted, 'model':model})

def pag_articole_sportive(request, pk):
    date_posted = datetime.datetime.now().year
    model = AnuntCopil.objects.get(id=pk)
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/pag_articole_sportive_copil.html", context)

def schimburi_copil(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_COPIL[4][1]
    model = AnuntCopil.objects.filter(categorie_copil = categorie)
    return render(request, "my_app/schimburi_copil.html", {'date_posted':date_posted, 'model':model})

def pag_schimburi_copil(request, pk):
    date_posted = datetime.datetime.now().year
    model = AnuntCopil.objects.get(id=pk)
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/schimburi_copil.html", context)

def mama_si_copil(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_COPIL[5][1]
    model = AnuntCopil.objects.filter(categorie_copil = categorie)
    return render(request, "my_app/mama_si_copil.html", {'date_posted':date_posted, 'model':model})

def pag_mama_si_copil(request, pk):
    date_posted = datetime.datetime.now().year
    model = AnuntCopil.objects.get(id=pk)
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/pag_mama_si_copil.html", context)

###############JUDETE################################

def judet_alba_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[0][1]
    model = AnuntCopil.objects.filter(localizare = judet)
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, 'my_app/judet_alba_copil.html', context)

def judet_arad_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[1][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_arad_copil.html", context)

def judet_arges_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[2][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'model':model,
        'date_posted':date_posted,
    }
    return render(request, "my_app/judet_arges_copil.html", context)

def judet_bacau_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[3][1]
    try:
        model = AnuntCopil.objects.filter(localizare = judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_bacau_copil.html", context)

def judet_bihor_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[4][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, "my_app/judet_bihor_copil.html", context)

def judet_bistrita_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[5][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, "my_app/judet_bistrita_copil.html", context)

def judet_botosani_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[6][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_botosani_copil.html", context)

def judet_braila_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[7][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, "my_app/judet_braila_copil.html", context)

def judet_brasov_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[8][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, "my_app/judet_brasov_copil.html", context)

def judet_buzau_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[9][1]
    model = AnuntCopil.objects.filter(localizare=judet)
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_buzau_copil.html", context)

def judet_calarasi_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[10][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_calarasi_copil.html", context)

def judet_caras_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[11][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, "my_app/judet_caras_copil.html", context)

def judet_cluj_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[12][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, "my_app/judet_cluj_copil.html", context)

def judet_constanta_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[13][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_constanta_copil.html", context)

def judet_covasna_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[14][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_covasna_copil.html", context)

def judet_dambovita_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[15][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_dambovita_copil.html", context)

def judet_dolj_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[16][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_dolj_copil.html", context)

def judet_galati_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[17][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_galati_copil.html", context)

def judet_giurgiu_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[18][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_giurgiu_copil.html", context)

def judet_gorj_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[19][1]
    try:
        model = AnuntCopil.objects.filter(localizare = judet)
    except:
        return Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, "my_app/judet_gorj_copil.html", context)

def judet_harghita_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[20][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, "my_app/judet_harghita_copil.html", context)

def judet_hunedoara_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[21][1]
    try:
        model = AnuntCopil.objects.filter(localizare = judet)
    except:
        return Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, "my_app/judet_hunedoara_copil.html", context)

def judet_bucuresti_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[24][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, "my_app/judet_bucuresti_copil.html", context)

def judet_ialomita_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[22][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, "my_app/judet_ialomita_copil.html", context)

def judet_iasi_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[23][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, "my_app/judet_iasi_copil.html", context)

def judet_maramures_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[25][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_maramures_copil.html", context)

def judet_mehedinti_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[26][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_mehedinti_copil.html", context)

def judet_mures_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[27][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_mures_copil.html", context)

def judet_neamt_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[28][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_neamt_copil.html", context)

def judet_olt_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[29][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_olt_copil.html", context)

def judet_prahova_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[30][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_prahova_copil.html", context)

def judet_salaj_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[31][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_salaj_copil.html", context)

def judet_satu_mare_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[32][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_satu_mare_copil.html", context)

def judet_sibiu_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[33][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_sibiu_copil.html", context)

def judet_suceava_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[34][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_suceava_copil.html", context)

def judet_teleorman_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[35][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_teleorman_copil.html", context)

def judet_timis_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[36][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_timis_copil.html", context)

def judet_tulcea_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[37][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_tulcea_copil.html", context)

def judet_valcea_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[38][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_valcea_copil.html", context)

def judet_vaslui_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[39][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_vaslui_copil.html", context)

def judet_vrancea_copil(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[40][1]
    try:
        model = AnuntCopil.objects.filter(localizare=judet)
    except:
        return Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/judet_vrancea_copil.html", context)

def anunturi_postate_copil(request):
    model = AnuntCopil.objects.all()
    date_posted = datetime.datetime.now().year
    p = Paginator(AnuntCopil.objects.all(), 26)
    page = request.GET.get('page')
    anunturile = p.get_page(page)
    myFilter = SearchFilter(request.GET, queryset=model)
    model = myFilter.qs
    if request.method == "POST":
        cautat = request.POST['cautat']
        model_cautat = AnuntCopil.objects.filter(categorie_adult = cautat)
        return render(request, "my_app/base_copil.html", {'cautat':cautat, 'model_cautat':model_cautat, 'model':model, 'date_posted':date_posted, 'anunturile':anunturile, 'myFilter':myFilter})
    else:
        return render(request, "my_app/base_copil.html", {'model':model, 'date_posted':date_posted, 'anunturile':anunturile, 'myFilter':myFilter})

def search_copil(request):
    date_posted = datetime.datetime.now().year
    if request.method == "POST":
        cautat = request.POST.get("cautat")
        model_cautat = AnuntCopil.objects.filter(categorie_copil__contains = cautat)
        return render(request, 'my_app/cautare_copil.html', {'date_posted':date_posted, 'model_cautat':model_cautat, 'cautat':cautat})
    else:
        raise Http404
        

#########################################
#############ADULT#######################
#########################################

def inregistrare_adult(request):
    date_posted = datetime.datetime.now().year
    form = AdultForm()
    if request.method == "POST":
        form = AdultForm(request.POST)
        if form.is_valid():
            user = form.save()
            Adult.objects.create(
                user=user,
                nume=user.username,
            )
            return redirect("my_app:autentificate_adult")
        else:
            messages.warning(request, "Parola este prea scurta! Pentru a va imbunatatii parola folositi minim 8 caractere, numere si semne de punctuatie!")
    return render(request, "my_app/inregistrare_adult.html", {"form":form, "date_posted":date_posted})

def autentificate_adult(request):
    date_posted = datetime.datetime.now().year
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('my_app:contul_meu_adult')
        else:
            messages.warning(request, "Numele sau parola sunt incorecte!")
    context = {
        'date_posted':date_posted,
    }
    return render(request, 'my_app/autentificate_adult.html', context)

###############CONTUL_MEU##################

@login_required()
def contul_meu_adult(request):
    date_posted = datetime.datetime.now().year
    model_anunt = AnuntAdult()
    data_anunt = datetime.datetime.now()
    return render(request, "my_app/contul_meu_adult.html", {'date_posted':date_posted, 'model_anunt':model_anunt, 'data_anunt':data_anunt})

@login_required
def conversatii_adult(request):
    date_posted = datetime.datetime.now().year
    context = {
        'date_posted':date_posted,
    }
    return render(request, "my_app/conversatii_adult.html", context)

def adauga_anunturi_favorite_d(request, pk):
    anunt = get_object_or_404(AnuntAdult, id=request.POST.get('favorit'))
    favorit_id = False
    if anunt.favorit.filter(id=request.user.id).exists():
        anunt.favorit.remove(request.user)
        favorit_id = True
    else:
        anunt.favorit.add(request.user)
        favorit_id = False
    return HttpResponseRedirect(reverse("my_app:pag_anunturi_postate_adult", args=[str(pk)]))

@login_required
def anunturi_favorite_d(request):
    date_posted = datetime.datetime.now().year
    user = request.user
    anunt_favorit = user.favorit.all()
    context = {
        'date_posted':date_posted,
        'anunt_favorit':anunt_favorit
    }
    return render(request, "my_app/anunturi_favorite_d.html", context)

@login_required
def actualizeaza_date_adult(request):
    date_posted = datetime.datetime.now().year
    model = request.user.adult
    form = Adult_ReForm(instance=model)
    if request.method == "POST":
        form = Adult_ReForm(request.POST, request.FILES, instance=model)
        if form.is_valid():
            form.save()
        else:
            form = Adult_ReForm()
    context = {
        'model':model,
        'form':form,
        'date_posted':date_posted,
    }
    return render(request, "my_app/actualizeaza_date_adult.html", context)


@login_required
def schimb_parola_adult(request):
    date_posted = datetime.datetime.now().year
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        model = User(password1=password1, password2=password2)
        model.save()
    context = {
        'date_posted':date_posted
    }
    return render(request, "my_app/schimb_parola_adult.html", context)

##################CRUD######################

@login_required
def pag_update_adult(request):
    date_posted = datetime.datetime.now().year
    model = AnuntAdult.objects.all()
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, "my_app/pag_update_adult.html", context)

@login_required
def UpdateAdult(request, pk):
    date_posted = datetime.datetime.now().year
    form = AnuntAdultForm()
    if request.method == "POST":
        form = AnuntAdultForm(request.POST)
        if form.is_valid():
            form.save()
    if request.method == "POST":
        user = User.objects.get(id=pk)
        titlul = request.POST.get("titlul")
        numele_anuntului = request.POST.get('numele_anuntului')
        descriere = request.POST.get("descriere")
        categorie_adult = request.POST.get("categorie_adult")
        subcategorie_adult = request.POST.get("subcategorie_adult")
        telefon = request.POST.get("telefon")
        email = request.POST.get("email")
        pret = request.POST.get("pret")
        moneda = request.POST.get("moneda")
        imagine = request.FILES.get("imagine")
        imagine2 = request.FILES.get("imagine2")
        imagine3 = request.FILES.get("imagine3")
        imagine4 = request.FILES.get("imagine4")
        imagine5 = request.FILES.get("imagine5")
        imagine6 = request.FILES.get("imagine6")
        localizare = request.POST.get("localizare")
        ########Autoturisme########
        caroserie = request.POST.get("caroserie")
        capacitate_motor = request.POST.get("capacitate_motor")
        combustibil = request.POST.get("combustibil")
        culoare = request.POST.get("culoare")
        cutie_de_viteze = request.POST.get("cutie_de_viteze")
        marca = request.POST.get("marca")
        rulaj = request.POST.get("rulaj")
        stare = request.POST.get("stare")
        #########Imobiliare########
        numar_de_camere = request.POST.get("numar_de_camere")
        compartimentare = request.POST.get("compartimentare")
        suprafata_utila = request.POST.get("suprafata_utila")
        an_de_constructie = request.POST.get("an_de_constructie")
        etaj = request.POST.get("etaj")
        teren = request.POST.get("teren")
        ##########Moda#############
        marime = request.POST.get("marime")
        ##########Locuri###########
        tip_job = request.POST.get("tip_job")
        tip_contract = request.POST.get("tip_contract")
        nivelul_de_studii = request.POST.get("nivelul_de_studii")
        nivelul_de_experienta = request.POST.get("nivelul_de_experienta")
        mobilitatea_postului = request.POST.get("mobilitatea_postului")
        program_flexibil = request.POST.get("program_flexibil")
        model = AnuntAdult(user=user, titlul=titlul,numele_anuntului=numele_anuntului, descriere=descriere, categorie_adult=categorie_adult, subcategorie_adult=subcategorie_adult, telefon=telefon, email=email, pret=pret, moneda=moneda,
                            caroserie=caroserie, 
                            capacitate_motor=capacitate_motor,combustibil=combustibil,culoare=culoare,cutie_de_viteze=cutie_de_viteze, marca=marca,rulaj=rulaj,stare=stare,
                            numar_de_camere=numar_de_camere, compartimentare=compartimentare,suprafata_utila=suprafata_utila,an_de_constructie=an_de_constructie,etaj=etaj,teren=teren,
                            marime=marime,
                            tip_job=tip_job,tip_contract=tip_contract,nivelul_de_studii=nivelul_de_studii,nivelul_de_experienta=nivelul_de_experienta,mobilitatea_postului=mobilitatea_postului,program_flexibil=program_flexibil,
                            imagine=imagine, localizare=localizare, imagine2=imagine2, imagine3=imagine3, imagine4=imagine4, imagine5=imagine5, imagine6=imagine6)
        model.save()
    context = {
        'form':form,
        'date_posted':date_posted,
    }
    return render(request, 'my_app/update_adult.html', context)

@login_required
def pag_delete_adult(request):
    date_posted = datetime.datetime.now().year
    model = AnuntAdult.objects.all()
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, "my_app/pag_delete_adult.html", context)

@login_required
def DeleteAdult(request, pk):
    model = AnuntAdult.objects.get(id=pk)
    date_posted = datetime.datetime.now().year
    if request.method == "POST":
        model.delete()
        return redirect('my_app/contul_meu_adult')
    context = {
        'model':model,
        'date_posted':date_posted,
    }
    return render(request, 'my_app/delete_adult.html', context)

############################################

@login_required
def anunturi_totale_adult(request, pk):
    date_posted = datetime.datetime.now().year
    user_model = User.objects.get(id=pk)
    anunt = user_model.anuntadult_set.all()
    afacere = user_model.afacere_set.all()
    serviciu = user_model.serviciu_set.all()
    context = {
        'date_posted':date_posted,
        'anunt':anunt,
        'user_model':user_model,
        'afacere':afacere,
        'serviciu':serviciu,
    }
    return render(request, "my_app/anunturi_totale_adult.html", context)

@login_required
def posteaza_anunt_adult(request, pk):
    date_posted = datetime.datetime.now().year
    form = AnuntAdultForm()
    if request.method == "POST":
        form = AnuntAdultForm(request.POST)
        if form.is_valid():
            form.save()
    if request.method == "POST":
        user = User.objects.get(id=pk)
        titlul = request.POST.get("titlul")
        numele_anuntului = request.POST.get('numele_anuntului')
        descriere = request.POST.get("descriere")
        categorie_adult = request.POST.get("categorie_adult")
        subcategorie_adult = request.POST.get("subcategorie_adult")
        telefon = request.POST.get("telefon")
        email = request.POST.get("email")
        pret = request.POST.get("pret")
        moneda = request.POST.get("moneda")
        imagine = request.FILES.get("imagine")
        imagine2 = request.FILES.get("imagine2")
        imagine3 = request.FILES.get("imagine3")
        imagine4 = request.FILES.get("imagine4")
        imagine5 = request.FILES.get("imagine5")
        imagine6 = request.FILES.get("imagine6")
        localizare = request.POST.get("localizare")
        ########Autoturisme########
        caroserie = request.POST.get("caroserie")
        capacitate_motor = request.POST.get("capacitate_motor")
        combustibil = request.POST.get("combustibil")
        culoare = request.POST.get("culoare")
        cutie_de_viteze = request.POST.get("cutie_de_viteze")
        marca = request.POST.get("marca")
        rulaj = request.POST.get("rulaj")
        stare = request.POST.get("stare")
        #########Imobiliare########
        numar_de_camere = request.POST.get("numar_de_camere")
        compartimentare = request.POST.get("compartimentare")
        suprafata_utila = request.POST.get("suprafata_utila")
        an_de_constructie = request.POST.get("an_de_constructie")
        etaj = request.POST.get("etaj")
        teren = request.POST.get("teren")
        ##########Moda#############
        marime = request.POST.get("marime")
        ##########Locuri###########
        tip_job = request.POST.get("tip_job")
        tip_contract = request.POST.get("tip_contract")
        nivelul_de_studii = request.POST.get("nivelul_de_studii")
        nivelul_de_experienta = request.POST.get("nivelul_de_experienta")
        mobilitatea_postului = request.POST.get("mobilitatea_postului")
        program_flexibil = request.POST.get("program_flexibil")
        model = AnuntAdult(user=user, titlul=titlul,numele_anuntului=numele_anuntului, descriere=descriere, categorie_adult=categorie_adult, subcategorie_adult=subcategorie_adult, telefon=telefon, email=email, pret=pret, moneda=moneda,
                            caroserie=caroserie, 
                            capacitate_motor=capacitate_motor,combustibil=combustibil,culoare=culoare,cutie_de_viteze=cutie_de_viteze, marca=marca,rulaj=rulaj,stare=stare,
                            numar_de_camere=numar_de_camere, compartimentare=compartimentare,suprafata_utila=suprafata_utila,an_de_constructie=an_de_constructie,etaj=etaj,teren=teren,
                            marime=marime,
                            tip_job=tip_job,tip_contract=tip_contract,nivelul_de_studii=nivelul_de_studii,nivelul_de_experienta=nivelul_de_experienta,mobilitatea_postului=mobilitatea_postului,program_flexibil=program_flexibil,
                            imagine=imagine, localizare=localizare, imagine2=imagine2, imagine3=imagine3, imagine4=imagine4, imagine5=imagine5, imagine6=imagine6)
        model.save()
    context = {
        'date_posted':date_posted,
        'form':form,
    }
    return render(request, "my_app/posteaza_anunt_adult.html", context)

@login_required
def deconectare_adult1(request):
    date_posted = datetime.datetime.now().year
    return render(request, "my_app/deconectare_adult1.html", {'date_posted':date_posted})

@login_required
def deconectare_adult(request):
    logout(request)
    return HttpResponseRedirect(reverse('anunturi_postate_adult'))

def pag_anunturi_postate_adult(request, pk):
    date_posted = datetime.datetime.now().year
    anunt = AnuntAdult.objects.get(id=pk)
    model = AnuntAdult.objects.filter(id=pk)
    favorit_id = False
    if anunt.favorit.filter(id=request.user.id).exists():
        favorit_id = True
    context = {
        'date_posted':date_posted,
        'model':model,
        'anunt':anunt,
        'favorit_id':favorit_id,
    }
    return render(request, "my_app/pag_anunturi_postate_adult.html", context)

def cautare_anunt(request):
    model = AnuntAdult.objects.all()
    new_model = AnuntAdult.objects.count()
    model_afacere = Afacere.objects.all().order_by("?")
    model_serviciu = Serviciu.objects.all().order_by("?")
    date_posted = datetime.datetime.now().year
    p = Paginator(AnuntAdult.objects.all(), 26)
    page = request.GET.get('page')
    anunturile = p.get_page(page)
    myFilter = SearchFilter(request.GET, queryset=model)
    model = myFilter.qs
    if request.method == "POST":
        cautat = request.POST['cautat']
        lookup = (Q(localizare__icontains = cautat) and Q(categorie_adult__icontains = cautat))
        model_cautat = AnuntAdult.objects.filter(lookup)
        return render(request, "my_app/anunturi_postate_adult.html", {'cautat':cautat, 'model_cautat':model_cautat, 'model':model, 'date_posted':date_posted, 'anunturile':anunturile, 'myFilter':myFilter, 'new_model':new_model})
    else:
        return render(request, "my_app/anunturi_postate_adult.html", {'model':model, 'date_posted':date_posted, 'anunturile':anunturile, 'myFilter':myFilter, 'new_model':new_model, 'model_afacere':model_afacere, 'model_serviciu':model_serviciu})

#################CATEGORII_ADULT###############

def auto_adult(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_ADULT[0][0]
    model = AnuntAdult.objects.filter(categorie_adult = categorie)
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, "my_app/auto_adult.html", context)

def specificatii_auto(request):
    if request.method == "POST":
        caroserie = request.POST.get("caroserie")
        combustibil = request.POST.get("combustibil")
        culoare = request.POST.get("culoare")
        cutie_de_viteze = request.POST.get("cutie_de_viteze")
        marca = request.POST.get("marca")
        rulaj = request.POST.get("rulaj")
        stare = request.POST.get("stare")
        pret = CATEGORIE_ADULT[0][0]
        lookup = (Q(caroserie__icontains=caroserie) or Q(combustibil__icontains=combustibil) or Q(culoare__icontains=culoare) or Q(cutie_de_viteze__icontains=cutie_de_viteze) or Q(marca_icontains=marca) or Q(rulaj__icontains=rulaj) or Q(stare__icontains=stare) or Q(pret__icontains=pret))
        new_model = AnuntAdult.objects.filter(lookup)
        return render(request, "my_app/specificatii_auto.html", {'new_model':new_model})
    else:
        return HttpResponseRedirect(reverse("my_app:anunturi_postate_adult"))

def autoturisme(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[0][0]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, "my_app/autoturisme.html", context)

def ambarcatiuni(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[0][1]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/ambarcatiuni_adult.html', context)

def autoutilitare(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[0][2]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/autoutilitare_adult.html", context)

def camioane_rulote_remorci(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[0][3]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/camioane_adult.html', context)

def motociclete_scutere_atv(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[0][4]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, "my_app/motociclete_adult.html", context)

def piese_auto(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_ADULT[1][1]
    model = AnuntAdult.objects.filter(categorie_adult = categorie)
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, "my_app/piese_auto_adult.html", context)

def specificatii_piese(request):
    if request.method == "POST":
        date_posted = datetime.datetime.now().year
        stare = request.POST.get("stare")
        pret = CATEGORIE_ADULT[1][0]
        lookup = (Q(stare__icontains = stare) or Q(pret__icontains=pret))
        model = AnuntAdult.objects.filter(lookup)
        context = {
            'date_posted':date_posted,
            'model':model,
        }
        return render(request, "my_app/specificatii_piese.html", context)
    else:
        raise Http404

def roti_jante_anvelope(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[1][0]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/roti_adult.html', context)

def caroserie_interior(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[1][1]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/caroserie_adult.html", context)

def mecanica_electrica(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[1][2]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/mecanica_adult.html", context)

def agro_si_industrie(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_ADULT[2][0]
    model = AnuntAdult.objects.filter(categorie_adult = categorie)
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/agro_si_industrie.html", context)

def specificatii_agro(request):
    if request.method == "POST":
        stare = request.POST.get("stare")
        pret = CATEGORIE_ADULT[2][0]
        lookup = (Q(stare__icontains = stare) or Q(pret__icontains=pret))
        model = AnuntAdult.objects.filter(lookup)
        context = {
            'model':model
        }
        return render(request, "my_app/specificatii_agro.html", context)

def utilaje(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[2][0]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/utilaje_adult.html', context)

def animale_domestice(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[2][1]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/animale_adult.html', context)

def produse_piata(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[2][2]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/produse_adult.html', context)

def imobiliare(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_ADULT[3][1]
    model = AnuntAdult.objects.filter(categorie_adult = categorie)
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/imobiliare_adult.html', context)

def specificatii_imobiliare(request):
    if request.method == "POST":
        date_posted = datetime.datetime.now().year
        numar_de_camere = request.POST.get("numar_de_camere")
        compartimentare = request.POST.get("compartimentare")
        suprafata_utila = request.POST.get("suprafata_utila")
        an_de_constructie = request.POST.get("an_de_constructie")
        etaj = request.POST.get("etaj")
        teren = request.POST.get("teren")
        pret = CATEGORIE_ADULT[3][0]
        lookup = (Q(numar_de_camere__icontains = numar_de_camere) or Q(compartimentare__icontains=compartimentare) or Q(suprafata_utila__icontains=suprafata_utila) or Q(an_de_constructie__icontains=an_de_constructie) or Q(etaj__icontains=etaj) or Q(teren__icontains=teren) or Q(pret__icontains=pret))
        model = AnuntAdult.objects.filter(lookup)
        context = {
            'model':model,
            'date_posted':date_posted,
        }
        return render(request, "my_app/specificatii_imobiliare.html", context)

def apartamente_de_vanzare(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[3][0]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/apartamente_v_adult.html', context)

def apartamente_de_inchiriat(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[3][1]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/apartamente_i_adult.html', context)

def birouri(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[3][2]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/birouri.html', context)

def case_de_vanzare(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[3][3]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/case_de_vanzare.html', context)

def case_de_inchiriat(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[3][4]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/case_de_inchiriat.html', context)

def terenuri_agricole(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[3][5]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/terenuri_agricole.html', context)

def terenuri_constructii(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[3][6]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/terenuri_constructii.html', context)

def spatii_comerciale(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[3][7]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/spatii_comerciale.html', context)

def spatii_industriale(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[3][8]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/spatii_industriale.html', context)

def moda(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_ADULT[4][0]
    try:
        model = AnuntAdult.objects.filter(categorie_adult = categorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/moda_adult.html', context)

def specificatii_moda(request):
    if request.method == "POST":
        date_posted = datetime.datetime.now().year
        marca = request.POST.get("marca")
        stare = request.POST.get("stare")
        marime = request.POST.get("marime")
        culoare = request.POST.get("culoare")
        pret = CATEGORIE_ADULT[4][0]
        lookup = (Q(marca__icontains=marca) or Q(stare__icontains=stare) or Q(marime__icontains=marime) or Q(culoare__icontains=culoare) or Q(pret__icontains=pret))
        model = AnuntAdult.objects.filter(lookup)
        context = {
            'model':model,
            'date_posted':date_posted,
        }
        return render(request, "my_app/specificatii_moda.html", context)

def haine_dama(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[4][0]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/haine_dama.html', context)

def haine_barbati(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[4][1]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/haine_barbati.html", context)

def incaltaminte_dama(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[4][2]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/incaltaminte_dama.html", context)

def incaltaminte_barbati(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[4][3]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'model':model,
        'date_posted':date_posted,
    }
    return render(request, 'my_app/incaltaminte_barbati.html', context)

def bijuterii(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[4][4]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/bijuterii.html', context)

def cosmetice(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[4][5]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/cosmetice.html', context)

def accesorii(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[4][6]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/accesorii.html', context)

def electronice_si_electrocasnice(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_ADULT[5][0]
    try:
        model = AnuntAdult.objects.filter(categorie_adult = categorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/electronice_si_electrocasnice.html', context)

def specificatii_electronice(request):
    if request.method == "POST":
        date_posted = datetime.datetime.now().year
        stare = request.POST.get("stare")
        pret = CATEGORIE_ADULT[5][0]
        lookup = (Q(stare__icontains = stare) or Q(pret__icontains = pret))
        model = AnuntAdult.objects.filter(stare = lookup)
        context = {
            'date_posted':date_posted,
            'model':model
        }
        return render(request, "my_app/specificatii_electronice.html", context)

def telefoane_adult(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[5][0]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/telefoane_adult.html', context)

def tablete_adult(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[5][1]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/tablete_adult.html', context)

def electrocasnice(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[5][2]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/electrocasnice.html', context)

def laptop_calculator(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[5][3]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/laptop_calculator.html', context)

def aparate_foto(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[5][4]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/aparate_foto.html', context)

def console(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[5][5]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/console.html', context)

def afaceri_servicii(request):
    date_posted = datetime.datetime.now().year
    model = Afacere.objects.all()
    context = {
        'model':model,
        'date_posted':date_posted,
    }
    return render(request, "my_app/afaceri_servicii.html", context)

def cautare_afaceri(request):
    date_posted = datetime.datetime.now().year
    if request.method == "POST":
        tipul_afacerii = request.POST.get("tipul_afacerii")
        judet = request.POST.get("judet")
        lookup = (Q(tipul_afacerii__icontains = tipul_afacerii) or Q(judet__icontains = judet))
        model = Afacere.objects.filter(lookup)
        return render(request, "my_app/cautare_afaceri.html", {'model':model, 'date_posted':date_posted})
    else:
        return render(request, "my_app/cautare_afaceri.html", {'date_posted':date_posted})

def servicii(request):
    date_posted = datetime.datetime.now().year
    model = Serviciu.objects.all()
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, "my_app/servicii.html", context)

def cautare_servicii(request):
    date_posted = datetime.datetime.now().year
    if request.method == "POST":
        tipul_serviciului = request.POST.get("tipul_serviciului")
        judet = request.POST.get("judet")
        lookup = (Q(tipul_serviciului__icontains = tipul_serviciului) or Q(judet_icontains = judet))
        model = Serviciu.objects.filter(lookup)
        return render(request, "my_app/cautare_servicii.html", {'date_posted':date_posted, 'model':model})
    else:
        return render(request, "my_app/cautare_servicii.html", {'date_posted':date_posted})

def cafenele(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[6][0]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/cafenele.html', context)

def cofetarii(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[6][1]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/cofetarii.html', context)

def constructii(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[6][2]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/constructii.html', context)

def cabinete_medicale(request):
    date_posted = datetime.datetime.now()
    subcategorie = SUBCATEGORIE_ADULT[6][3]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/cabinete_medicale.html', context)

def fast_food(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[6][4]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, 'my_app/fast_food.html', context)

def restaurante(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[6][5]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/restaurante.html', context)

def contabilitate(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[6][6]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/contabilitate.html', context)

def digital_marketing(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[6][7]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/digitalmarkting.html', context)

def grafic_design(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[6][8]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/grafic_design.html', context)

def meditatii(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[6][9]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/meditatii.html', context)

def programare_si_tehnologie(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[6][10]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/programare_tehnologie.html', context)

def video_si_animatii(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[6][11]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/video_si_animatii.html', context)

def animale_de_companie(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_ADULT[7][0]
    try:
        model = AnuntAdult.objects.filter(categorie_adult = categorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/animale_de_companie.html', context)

def specificatii_animale(request):
    if request.method == "POST":
        date_posted = datetime.datetime.now().year
        pret = CATEGORIE_ADULT[7][0]
        lookup = Q(pret__icontains=pret)
        model = AnuntAdult.objects.filter(lookup)
        context = {
            'date_posted':date_posted,
            'model':model,
        }
        return render(request, "my_app/specificatii_animale.html", context)

def adoptii_animale(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[7][0]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'model':model,
        'date_posted':date_posted,
    }
    return render(request, 'my_app/adoptii_animale.html', context)

def accesorii_animale(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[7][1]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/accesorii_animale.html', context)

def locuri_de_munca(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_ADULT[8][0]
    try:
        model = AnuntAdult.objects.filter(categorie_adult = categorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/locuri_de_munca.html', context)

def specificatii_locuri(request):
    if request.method == "POST":
        date_posted = datetime.datetime.now().year
        tip_job = request.POST.get("tip_job")
        tip_contract = request.POST.get("tip_contract")
        nivelul_de_studii = request.POST.get("nivelul_de_studii")
        nivelul_de_experienta = request.POST.get("nivelul_de_experienta")
        mobilitatea_postului = request.POST.get("mobilitatea_postului")
        program_flexibil = request.POST.get("program_flexibil")
        lookup = (Q(tip_job__icontains=tip_job) or Q(tip_contract__icontains=tip_contract) or Q(nivelul_de_studii__icontains=nivelul_de_studii) or Q(nivelul_de_experienta__icontains=nivelul_de_experienta) or Q(mobilitatea_postului__icontains=mobilitatea_postului) or Q(program_flexibil__icontains=program_flexibil))
        model = AnuntAdult.objects.filter(lookup)
        context = {
            'date_posted':date_posted,
            'model':model
        }
        return render(request, "my_app/specificatii_locuri.html", context)

def agenti_vanzari(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[8][0]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/agenti_vanzari.html', context)

def confectii(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[8][1]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/confectii/html', context)

def cosmeticieni(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[8][2]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/cosmeticieni.html', context)

def ingineri(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[8][3]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/ingineri.html', context)

def munca(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[8][4]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/munca.html', context)

def paza_si_protectie(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[8][5]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/paza_si_protectie.html', context)

def personal_hotelier(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[8][6]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/personal_hotelier.html', context)

def sport_timp_liber(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_ADULT[9][0]
    try:
        model = AnuntAdult.objects.filter(categorie_adult = categorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/sport_timp_liber.html', context)

def specificatii_sport(request):
    if request.method == "POST":
        date_posted = datetime.datetime.now().year
        pret = CATEGORIE_ADULT[9][0]
        lookup = Q(pret__icontains = pret)
        model = AnuntAdult.objects.filter(lookup)
        context = {
            'model':model,
            'date_posted':date_posted,
        }
        return render(request, "my_app/specificatii_sport.html", context)

def articole_sportive_adult(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[9][0]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/articole_sportive_adult.html', context)

def carti_filme(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[9][1]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/carti_filme.html', context)

def arta_antichitati(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[9][2]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/arta_antichitati.html', context)

def muzica_adult(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[9][3]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/muzica_adult.html', context)

def search_adult(request):
    date_posted = datetime.datetime.now().year
    model = AnuntAdult.objects.all().order_by("id")
    if request.method == "POST":
        cautat = request.POST['cautat']
        lookup = (Q(numele_anuntului__icontains = cautat))
        model_cautat = AnuntAdult.objects.filter(lookup)
        return render(request, 'my_app/cautare_adult.html', {'date_posted':date_posted, 'model_cautat':model_cautat, 'cautat':cautat, 'model':model})
    else:
        raise Http404
        
######################JUDETE_ADULT####################

def judet_alba_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[0][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_alba_adult.html', context)

def judet_arad_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[1][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_arad_adult.html', context)

def judet_arges_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[2][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_arges_adult.html', context)

def judet_bacau_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[3][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_bacau_adult.html', context)

def judet_bihor_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[4][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_bihor_adult.html', context)

def judet_bistrita_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[5][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_bistrita_adult.html', context)

def judet_botosani_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[6][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_botosani_adult.html', context)

def judet_braila_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[7][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/judet_braila_adult.html', context)

def judet_brasov_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[8][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_brasov_adult.html', context)

def judet_buzau_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[9][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_buzau_adult.html', context)

def judet_calarasi_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[10][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_calarasi_adult.html', context)

def judet_caras_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[11][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_caras_adult.html', context)

def judet_cluj_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[12][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_cluj_adult.html', context)

def judet_constanta_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[13][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, 'my_app/judet_constanta_adult.html', context)

def judet_covasna_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[14][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_covasna_adult.html', context)

def judet_dambovita_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[15][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_dambovita_adult.html', context)

def judet_dolj_adult(request):
    date_posted = datetime.datetime.now().year
    judet  = JUDETE[16][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_dolj_adult.html', context)

def judet_galati_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[17][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_galati_adult.html', context)

def judet_giurgiu_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[18][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'model':model,
        'date_posted':date_posted
    }
    return render(request, 'my_app/judet_giurgiu_adult.html', context)

def judet_gorj_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[19][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_gorj_adult.html', context)

def judet_harghita_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[20][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_harghita_adult.html', context)

def judet_hunedoara_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[21][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_hunedoara_adult.html', context)

def judet_ialomita_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[22][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_ialomita_adult.html', context)

def judet_iasi_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[23][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/judet_iasi_adult.html', context)

def judet_ilfov_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[24][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/judet_ilfov_adult.html', context)

def judet_maramures_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[25][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/jduet_maramures_adult.html', context)

def judet_mehedinti_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[26][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_mehedinti_adult.html', context)

def judet_mures_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[27][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/judet_mures_adult.html', context)

def judet_neamt_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[28][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_neamt_adult.html', context)

def judet_olt_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[29][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_olt_adult.html', context)

def judet_prahova_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[30][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_prahova_adult.html', context)

def judet_salaj_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[31][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_salaj_adult.html', context)

def judet_satu_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[32][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_satu_adult.html', context)

def judet_sibiu_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[33][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_sibiu_adult.html', context)

def judet_suceava_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[34][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_suceava_adult.html', context)

def judet_teleorman_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[35][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_teleorman_adult.html', context)

def judet_timis_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[36][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_timis_adult.html', context)

def judet_tulcea_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[37][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_tulcea_adult.html', context)

def judet_valcea_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[38][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_valcea_adult.html', context)

def judet_vaslui_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[39][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_vaslui_adult.html', context)

def judet_vrancea_adult(request):
    date_posted = datetime.datetime.now().year
    judet = JUDETE[40][0]
    try:
        model = AnuntAdult.objects.filter(localizare = judet)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, 'my_app/judet_vrancea_adult.html', context)

def promoveazati_afacerea_serviciul(request):
    date_posted = datetime.datetime.now().year
    context = {
        'date_posted':date_posted
    }
    return render(request, 'my_app/promoveazati_afacerea_serviciul.html', context)

def promoveazati_afacerea(request):
    date_posted = datetime.datetime.now().year
    if request.method == "POST":
        titlul = request.POST.get("titlul")
        numele_firmei = request.POST.get('numele_firmei')
        descriere = request.POST.get("descriere")
        judet = request.POST.get("judet")
        adresa = request.POST.get("adresa")
        email = request.POST.get("email")
        telefon = request.POST.get("telefon")
        tipul_afacerii = request.POST.get("tipul_afacerii")
        imagine = request.FILES.get("imagine")
        imagine2 = request.FILES.get("imagine2")
        imagine3 = request.FILES.get("imagine3")
        imagine4 = request.FILES.get("imagine4")
        imagine5 = request.FILES.get("imagine5")
        imagine6 = request.FILES.get("imagine6")
        model = Afacere(titlul=titlul,numele_firmei=numele_firmei,telefon=telefon, descriere=descriere, judet=judet, adresa=adresa, email=email, tipul_afacerii=tipul_afacerii, imagine=imagine,imagine2=imagine2, imagine3=imagine3, imagine4=imagine4, imagine5=imagine5, imagine6=imagine6)
        model.save()
    context = {
        'date_posted':date_posted
    }
    return render(request, 'my_app/promoveazati_afacerea.html', context)

def promoveazati_serviciul(request):
    date_posted = datetime.datetime.now().year
    if request.method == "POST":
        titlul = request.POST.get('titlul')
        numele_serviciului = request.POST.get('numele_serviciului')
        descriere = request.POST.get('descriere')
        tipul_serviciului = request.POST.get('tipul_serviciului')
        judet = request.POST.get('judet')
        email = request.POST.get('email')
        experienta_profesionala = request.POST.get('experienta_profesionala')
        telefon = request.POST.get('telefon')
        imagine = request.FILES.get('imagine')
        imagine2 = request.FILES.get('imagine2')
        imagine3 = request.FILES.get('imagine3')
        imagine4 = request.FILES.get('imagine4')
        imagine5 = request.FILES.get('imagine5')
        imagine6 = request.FILES.get('imagine6')
        model = Serviciu(titlul=titlul,telefon=telefon, numele_serviciului=numele_serviciului, descriere=descriere, tipul_serviciului=tipul_serviciului, judet=judet, email=email, experienta_profesionala=experienta_profesionala,imagine=imagine, imagine2=imagine2, imagine3=imagine3, imagine4=imagine4, imagine5=imagine5, imagine6=imagine6)
        model.save()
    context = {
        'date_posted':date_posted,
    }
    return render(request, 'my_app/promoveazati_serviciul.html', context)

def pag_anunturi_adult(request, pk):
    date_posted = datetime.datetime.now().year
    model = AnuntAdult.objects.get(id=pk)
    new_model = AnuntAdult.objects.all()
    context = {
        'date_posted':date_posted,
        'model':model,
        'new_model':new_model,
    }
    return render(request, 'my_app/pag_anunturi_adult.html', context)

def intreprinzatori_autohtoni(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_ADULT[10][0]
    try:
        model = AnuntAdult.objects.filter(categorie_adult = categorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, 'my_app/intreprinzatori.html', context)

def producatori_legume(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[10][0]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, "my_app/producatori_legume.html", context)

def crescatori_animale(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[10][1]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/crescatori_animale.html", context)

def microintreprinderi(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[10][2]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
    }
    return render(request, "my_app/microintreprinderi.html", context)

def matrimoniale(request):
    date_posted = datetime.datetime.now().year
    categorie = CATEGORIE_ADULT[11][0]
    try:
        model = AnuntAdult.objects.filter(categorie_adult = categorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/matrimoniale.html", context)

def escorte(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[11][0]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/escorte.html", context)

def saloane_masaj(request):
    date_posted = datetime.datetime.now().year
    subcategorie = SUBCATEGORIE_ADULT[11][1]
    try:
        model = AnuntAdult.objects.filter(subcategorie_adult = subcategorie)
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model
    }
    return render(request, "my_app/saloane_masaj.html", context)

def pag_afaceri(request, pk):
    date_posted = datetime.datetime.now().year
    try:
        model = Afacere.objects.filter(id=pk)
        new_model = MesajAfaceri.objects.all()
        my_model = Afacere.objects.all()
        form = MesajAfaceriForm()
        if request.method == "POST":
            form = MesajAfaceriForm(request.POST)
            if form.is_valid():
                form.save()
        if request.method == "POST":
            nume = request.POST.get('nume5')
            email = request.POST.get('email5')
            email2 = request.POST.get('email5')
            mesaj = request.POST.get('mesaj5')
            send_mail(
                'Maglo',
                mesaj,
                email,
                email2
            )
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
        'form':form,
    }
    return render(request, "my_app/pag_afaceri.html", context)

def pag_servicii(request, pk):
    date_posted = datetime.datetime.now().year
    try:
        model = Serviciu.objects.filter(id=pk)
        new_model = MesajServiciu.objects.all()
        form = MesajServiciuForm()
        if request.method == "POST":
            form = MesajServiciuForm(request.POST)
            if form.is_valid():
                form.save()
        if request.method == "POST":
            nume = request.POST.get('nume6')
            email = request.POST.get('email6')
            email2 = request.POST.get('email6')
            mesaj = request.POST.get('mesaj6')
            send_mail(
                'Maglo',
                mesaj,
                email,
                email2
            )
    except:
        raise Http404
    context = {
        'date_posted':date_posted,
        'model':model,
        'form':form,
    }
    return render(request, "my_app/pag_servicii.html", context)

# Create your views here.
