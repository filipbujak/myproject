from django.urls import path
from . import views

urlpatterns = [
    path("", views.strona_glowna, name="strona_glowna"),
    path("api/produkcje/", views.api_produkcje, name="api_produkcje"),
]