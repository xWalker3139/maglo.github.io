from django.contrib import admin
from .models import Adult, Copil, AnuntAdult, AnuntCopil, AjutorSiContact, MesajCopil, Afacere, Serviciu, MesajAfaceri, MesajServiciu, Mesaj_Copil

admin.site.register(Adult)
admin.site.register(Copil)
admin.site.register(AnuntCopil)
admin.site.register(AnuntAdult)
admin.site.register(AjutorSiContact)
admin.site.register(MesajCopil)
admin.site.register(Afacere)
admin.site.register(Serviciu)
admin.site.register(MesajAfaceri)
admin.site.register(MesajServiciu)
admin.site.register(Mesaj_Copil)

# Register your models here.
