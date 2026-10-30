from django.contrib import admin
from .models import Produkcja


@admin.register(Produkcja)
class ProdukcjaAdmin(admin.ModelAdmin):
    list_display = ("tytul", "typ", "uniwersum", "gatunek", "rok_wydania")
    list_filter = ("uniwersum", "typ")
    search_fields = ("tytul",)