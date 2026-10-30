from django.contrib import admin
from .models import Gra


@admin.register(Gra)
class GraAdmin(admin.ModelAdmin):
    list_display = ("tytul", "gatunek", "rok_wydania", "cena", "dostepna")
    list_filter = ("dostepna", "gatunek")
    search_fields = ("tytul",)