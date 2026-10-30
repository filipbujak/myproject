from django.http import JsonResponse
from django.shortcuts import render

from .models import Gra


def strona_glowna(request):
    return render(request, "katalog/index.html")


def api_gry(request):
    gry = Gra.objects.all()

    dostepna = request.GET.get("dostepna")
    if dostepna == "true":
        gry = gry.filter(dostepna=True)
    elif dostepna == "false":
        gry = gry.filter(dostepna=False)

    items = []
    for gra in gry:
        items.append({
            "id": gra.id,
            "tytul": gra.tytul,
            "opis": gra.opis,
            "gatunek": gra.gatunek,
            "rok_wydania": gra.rok_wydania,
            "cena": float(gra.cena),
            "dostepna": gra.dostepna,
            "data_dodania": gra.data_dodania.isoformat(),
        })

    return JsonResponse({"items": items})