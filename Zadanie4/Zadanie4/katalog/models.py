from django.db import models


class Gra(models.Model):
    tytul = models.CharField(max_length=100, verbose_name="Tytuł")
    opis = models.TextField(verbose_name="Opis")
    gatunek = models.CharField(max_length=50, verbose_name="Gatunek")
    rok_wydania = models.IntegerField(verbose_name="Rok wydania")
    cena = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cena")
    dostepna = models.BooleanField(default=True, verbose_name="Dostępna")
    data_dodania = models.DateField(auto_now_add=True, verbose_name="Data dodania")

    class Meta:
        verbose_name = "Gra"
        verbose_name_plural = "Gry"
        ordering = ["tytul"]

    def __str__(self):
        return f"{self.tytul} ({self.rok_wydania})"