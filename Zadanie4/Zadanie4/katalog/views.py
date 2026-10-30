from django.http import JsonResponse
from django.shortcuts import render

from .models import Produkcja


def strona_glowna(request):
    return render(request, "katalog/index.html")


def api_produkcje(request):

    produkcje = Produkcja.objects.all()


    uniwersum = request.GET.get("uniwersum")
    if uniwersum in dict(Produkcja.UNIWERSA):
        produkcje = produkcje.filter(uniwersum=uniwersum)

    typ = request.GET.get("typ")
    if typ in dict(Produkcja.TYPY):
        produkcje = produkcje.filter(typ=typ)

    items = []
    for p in produkcje:
        items.append({
            "id": p.id,
            "tytul": p.tytul,
            "typ": p.get_typ_display(),
            "rok_wydania": p.rok_wydania,
            "gatunek": p.gatunek,
            "uniwersum": p.get_uniwersum_display(),
            "opis": p.opis,
        })

    return JsonResponse({"items": items})