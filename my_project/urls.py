"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.conf.urls import url, include
from my_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^acasa/$', views.BaseView.as_view(), name="acasa"),
    url(r'^my_app/', include("my_app.urls")),
    url(r'^anunturi_postate_copil/$', views.anunturi_postate_copil, name="anunturi_postate_copil"),
    url(r'^deconectare_copil/$', views.deconectare_copil, name="deconectare_copil"),
    url(r'^contul_meu_copil/$', views.contul_meu_copil, name="contul_meu_copil"),

    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),


    #################ADULT###########

    url(r'^anunturi_postate_adult/$', views.cautare_anunt, name="anunturi_postate_adult"),
    url(r'^cautare/$', views.search_adult, name="search_adult"),
    url(r'^cautare_c/$', views.search_copil, name="search_copil"),


    ##############BAZA################

    url(r'^termeni_si_conditii/$', views.TermeniConditii.as_view(), name='termeni_si_conditii'),
    url(r'^ajutor_si_contact/$', views.AjutorSiContact, name="ajutor_si_contact"),
    url(r'^politica_de_confidentialitate/$',views.PoliticaDeConfidentialitate.as_view(), name="politica_confi"),
    url(r'^politica_de_cookie-uri/$', views.PoliticaDeCookieuri.as_view(), name="politica_cookie"),
    url(r'^protejeaza-te_pe_maglo/$', views.Securitate.as_view(), name='securitate'),

    url(r'', include("django.contrib.auth.urls")),

    ##################JUDETE##############
    url(r'^alba/$', views.judet_alba_copil, name="judet_alba_copil"),
    url(r'arad/$',views.judet_arad_copil, name="judet_arad_copil"),
    url(r'^arges/$', views.judet_arges_copil, name="judet_arges_copil"),
    url(r'^bacau/$', views.judet_bacau_copil, name="judet_bacau_copil"),
    url(r'^bihor/$', views.judet_bihor_copil, name="judet_bihor_copil"),
    url(r'^bistrita-nasaud/$', views.judet_bistrita_copil, name="judet_bistrita_copil"),
    url(r'^botosani/$', views.judet_botosani_copil, name="judet_botosani_copil"),
    url(r'^braila/$', views.judet_braila_copil, name="judet_braila_copil"),
    url(r'^brasov/$', views.judet_brasov_copil, name="judet_brasov_copil"),
    url(r'^bucuresti/$', views.judet_bucuresti_copil, name="judet_bucuresti_copil"),
    url(r'^buzau/$', views.judet_buzau_copil, name="judet_buzau_copil"),
    url(r'^calarasi/$', views.judet_calarasi_copil, name="judet_calarasi_copil"),
    url(r'^caras-severin/$', views.judet_caras_copil, name="judet_caras_copil"),
    url(r'^cluj/$', views.judet_cluj_copil, name="judet_cluj_copil"),
    url(r'^constanta/$', views.judet_constanta_copil, name="judet_constanta_copil"),
    url(r'^covasna/$', views.judet_covasna_copil, name="judet_covasna_copil"),
    url(r'^dambovita/$', views.judet_dambovita_copil, name="judet_dambovita_copil"),
    url(r'^dolj/$', views.judet_dolj_copil, name="judet_dolj_copil"),
    url(r'^galati/$', views.judet_galati_copil, name="judet_galati_copil"),
    url(r'^giurgiu/$', views.judet_giurgiu_copil, name="judet_giurgiu_copil"),
    url(r'^gorj/$', views.judet_gorj_copil, name="judet_gorj_copil"),
    url(r'^harghita/$', views.judet_harghita_copil, name="judet_harghita_copil"),
    url(r'^hunedoara/$', views.judet_hunedoara_copil, name="judet_hunedoara_copil"),
    url(r'^ialomita/$', views.judet_ialomita_copil, name="judet_ialomita_copil"),
    url(r'^iasi/$', views.judet_iasi_copil, name="judet_iasi_copil"),
    url(r'^maramures/$', views.judet_maramures_copil, name="judet_maramures_copil"),
    url(r'^mehedinti/$', views.judet_mehedinti_copil, name="judet_mehedinti_copil"),
    url(r'^mures/$', views.judet_mures_copil, name="judet_mures_copil"),
    url(r'^neamt/$', views.judet_neamt_copil, name="judet_neamt_copil"),
    url(r'^olt/$', views.judet_olt_copil, name="judet_olt_copil"),
    url(r'^prahova/$', views.judet_prahova_copil, name="judet_prahova_copil"),
    url(r'^salaj/$', views.judet_salaj_copil, name="judet_salaj_copil"),
    url(r'^satu_mare/$', views.judet_satu_mare_copil, name="judet_satu_mare_copil"),
    url(r'^sibiu/$', views.judet_sibiu_copil, name="judet_sibiu_copil"),
    url(r'^suceava/$', views.judet_suceava_copil, name="judet_suceava_copil"),
    url(r'^teleorman/$', views.judet_teleorman_copil, name="judet_teleorman_copil"),
    url(r'^timis/$', views.judet_timis_copil, name="judet_timis_copil"),
    url(r'^tulcea/$', views.judet_tulcea_copil, name="judet_tulcea_copil"),
    url(r'^valcea/$', views.judet_valcea_copil, name="judet_valcea_copil"),
    url(r'^vaslui/$', views.judet_vaslui_copil, name="judet_vaslui_copil"),
    url(r'^vrancea/$', views.judet_vrancea_copil, name="judet_vrancea_copil"),

    #################JUDETE_ADULT######################

    url(r'^alba1/$', views.judet_alba_adult, name="judet_alba_adult"),
    url(r'^arad1/$', views.judet_arad_adult, name="judet_arad_adult"),
    url(r'^arges1/$', views.judet_arges_adult, name="judet_arges_adult"),
    url(r'^bacau1/$', views.judet_bacau_adult, name="judet_bacau_adult"),
    url(r'^bihor1/$', views.judet_bihor_adult, name="judet_bihor_adult"),
    url(r'^bistrita-nasaud1/$', views.judet_bistrita_adult, name="judet_bistrita_adult"),
    url(r'^botosani1/$', views.judet_botosani_adult, name="judet_botosani_adult"),
    url(r'^braila1/$', views.judet_braila_adult, name="judet_braila_adult"),
    url(r'^brasov1/$', views.judet_brasov_adult, name="judet_brasov_adult"),
    url(r'^buzau1/$', views.judet_buzau_adult, name="judet_buzau_adult"),
    url(r'^calarasi1/$', views.judet_calarasi_adult, name="judet_calarasi_adult"),
    url(r'^caras-severin1/$', views.judet_caras_adult, name="judet_caras_adult"),
    url(r'^cluj1/$', views.judet_cluj_adult, name="judet_cluj_adult"),
    url(r'constanta1/$', views.judet_constanta_adult, name="judet_constanta_adult"),
    url(r'^covasna1/$', views.judet_covasna_adult, name="judet_covasna_adult"),
    url(r'^dambovita1/$', views.judet_dambovita_adult, name="judet_dambovita_adult"),
    url(r'^dolj1/$', views.judet_dolj_adult, name="judet_dolj_adult"),
    url(r'^galati1/$', views.judet_galati_adult, name="judet_galati_adult"),
    url(r'^giurgiu1/$', views.judet_giurgiu_adult, name="judet_giurgiu_adult"),
    url(r'^gorj1/$', views.judet_gorj_adult, name="judet_gorj_adult"),
    url(r'^harghita1/$', views.judet_harghita_adult, name="judet_harghita_adult"),
    url(r'^hunedoara1/$', views.judet_hunedoara_adult, name="judet_hunedoara_adult"),
    url(r'^ialomita1/$', views.judet_ialomita_adult, name="judet_ialomita_adult"),
    url(r'^iasi1/$', views.judet_iasi_adult, name="judet_iasi_adult"),
    url(r'^ilfov1/$', views.judet_ilfov_adult, name="judet_ilfov_adult"),
    url(r'^maramures1/$', views.judet_maramures_adult, name="judet_maramures_adult"),
    url(r'^mehedinti1/$', views.judet_mehedinti_adult, name="judet_mehedinti_adult"),
    url(r'^mures1/$', views.judet_mures_adult, name="judet_mures_adult"),
    url(r'^neamt1/$', views.judet_neamt_adult, name="judet_neamt_adult"),
    url(r'^olt1/$', views.judet_olt_adult, name="judet_olt_adult"),
    url(r'^prahova1/$', views.judet_prahova_adult, name="judet_prahova_adult"),
    url(r'^salaj1/$', views.judet_salaj_adult, name="judet_salaj_adult"),
    url(r'^satu_mare1/$', views.judet_satu_adult, name="judet_satu_adult"),
    url(r'^sibiu1/$', views.judet_sibiu_adult, name="judet_sibiu_adult"),
    url(r'^suceava1/$', views.judet_suceava_adult, name="judet_suceava_adult"),
    url(r'^teleorman1/$', views.judet_teleorman_adult, name="judet_teleorman_adult"),
    url(r'^timis1/$', views.judet_timis_adult, name="judet_timis_adult"),
    url(r'^tulcea1/$', views.judet_tulcea_adult, name="judet_tulcea_adult"),
    url(r'^valcea1/$', views.judet_valcea_adult, name="judet_valcea_adult"),
    url(r'^vaslui1/$', views.judet_vaslui_adult, name="judet_vaslui_adult"),
    url(r'^vrancea1/$', views.judet_vrancea_adult, name="judet_vrancea_adult"),

    ##############CHAT##############

    path('conversatii_adult_m/', views.conversatii_adult_m, name='conversatii_adult_m'),
    path('<str:room>/', views.room, name='room_m'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),

    url(r'^conversatii_adult_v/$', views.lobby, name="lobby"),
    url(r'^room_video/$', views.room_video, name="room_video"),
    url(r'^get_token/$', views.getToken),
    url(r'^create_member/$', views.createMember),
    url(r'^get_member/$', views.getMember),
    url(r'^delete_member/$', views.deleteMember),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
