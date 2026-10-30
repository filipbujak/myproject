import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Task


def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "completed": task.completed,
        "created_at": task.created_at.isoformat(),
    }



def task_list(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        wynik = []
        for task in tasks:
            task_dict = task_to_dict(task)
            wynik.append(task_dict)

        return JsonResponse(wynik, safe=False)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Niepoprawny JSON"}, status=400)

        title = data.get("title", "")

        if not isinstance(title, str):
            return JsonResponse({"error": "Nie został podany tekst"}, status=400)

        title = title.strip()
        if title == "":
            return JsonResponse({"error": "Tytuł nie może być pusty"}, status=400)

        task = Task.objects.create(title=title)
        return JsonResponse(task_to_dict(task), status=201)

    return JsonResponse({"error": "Metoda niedozwolona"}, status=405)



def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Zadanie nie istnieje"}, status=404)

    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Niepoprawny JSON"}, status=400)

        completed = data.get("completed")
        if not isinstance(completed, bool):
            return JsonResponse({"error": "Pole completed musi być true lub false"}, status=400)

        task.completed = completed
        task.save()
        return JsonResponse(task_to_dict(task))

    if request.method == "DELETE":
        task.delete()
        return JsonResponse({"deleted": task_id})

    return JsonResponse({"error": "Metoda niedozwolona"}, status=405)
def index(request):
    return render(request, "tasks/index.html")