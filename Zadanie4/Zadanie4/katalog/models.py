from django.db import models


class Produkcja(models.Model):
    TYPY = [
        ("film", "Film"),
        ("serial", "Serial"),
        ("special", "Special"),
    ]
    UNIWERSA = [
        ("mcu", "MCU"),
        ("fox", "Fox"),
        ("sony", "Sony"),
        ("inne", "Inne"),
    ]

    tytul = models.CharField(max_length=150, verbose_name="Tytuł")
    typ = models.CharField(max_length=10, choices=TYPY, verbose_name="Typ")
    rok_wydania = models.IntegerField(verbose_name="Rok wydania")
    gatunek = models.CharField(max_length=60, verbose_name="Gatunek")
    uniwersum = models.CharField(max_length=10, choices=UNIWERSA, verbose_name="Uniwersum")
    opis = models.TextField(verbose_name="Opis")

    class Meta:
        verbose_name = "Produkcja"
        verbose_name_plural = "Produkcje"
        ordering = ["rok_wydania", "tytul"]

    def __str__(self):
        return f"{self.tytul} ({self.rok_wydania})"