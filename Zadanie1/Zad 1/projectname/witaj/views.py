from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("Witaj w Django!")


def hello_name(request, name):
    return HttpResponse(f"Witaj, {name}!")


def hello_template(request, name):
    return render(request, "witaj/hello.html", {"name": name})


def current_time(request):
    teraz = datetime.now()
    return render(request, "witaj/time.html", {
        "data": teraz.strftime("%d.%m.%Y"),
        "godzina": teraz.strftime("%H:%M"),
    })