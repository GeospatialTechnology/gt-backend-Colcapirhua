from django.contrib import admin
#from .models import AdmMapa
from .models import Predio
from .models import Manzano

#admin.site.register(AdmMapa)


# Register your models here.
class PredioAdmin(admin.ModelAdmin):
    list_display = ("gid", "objectid", "dist", "codigo", "codsist", "shape_leng", "shape_area")
    ordering = ["objectid"]
    search_fields = ["codigo"]
    list_filter = ("objectid","codigo")

admin.site.register(Predio, PredioAdmin)
