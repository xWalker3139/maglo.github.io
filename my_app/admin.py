from django.contrib import admin
from .models import Adult, Copil, AnuntAdult, AnuntCopil, AjutorSiContact, MesajCopil, Afacere, Serviciu

admin.site.register(Adult)
admin.site.register(Copil)
admin.site.register(AnuntCopil)
admin.site.register(AnuntAdult)
admin.site.register(AjutorSiContact)
admin.site.register(MesajCopil)
admin.site.register(Afacere)
admin.site.register(Serviciu)

# Register your models here.
