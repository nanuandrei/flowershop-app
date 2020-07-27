from django.contrib import admin

# Register your models here.
from flori.models import Produse,Poze

class PozeAdminInline(admin.TabularInline):
    model = Poze

class ProduseAdmin(admin.ModelAdmin):
    inlines = (PozeAdminInline,)
    list_display=["nume","pret","stoc"]

admin.site.register(Produse,ProduseAdmin)



from flori.models import Comanda,Useri


class ComandaAdminInline(admin.TabularInline):
    model = Comanda

class UseriAdmin(admin.ModelAdmin):
    inlines = (ComandaAdminInline,)
    list_display=["user","adresa","telefon"]

admin.site.register(Useri,UseriAdmin)