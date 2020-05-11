from datetime import datetime

from django.db import models


class Zrodlo(models.Model):
    def __str__(self):
        return self.nazwa

    nazwa = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Zrodlo"
        verbose_name_plural = "Źródło"


class Dochod(models.Model):
    def __str__(self):
        return self.nazwa

    zrodlo = models.ForeignKey(Zrodlo, on_delete=models.CASCADE, null=True)

    nazwa = models.CharField(max_length=60)
    opis = models.TextField(blank=True)
    kwota = models.DecimalField(max_digits=9999999, decimal_places=2)
    data = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = "Dochod"
        verbose_name_plural = "Dochody"


class Kategoria(models.Model):
    def __str__(self):
        return self.nazwa

    nazwa = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"


class Wydatek(models.Model):
    def __str__(self):
        return self.nazwa

    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE, null=True)
    nazwa = models.CharField(max_length=60)
    opis = models.TextField(blank=True)
    kwota = models.DecimalField(max_digits=99999999, decimal_places=2)
    data = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = "Wydatek"
        verbose_name_plural = "Wydatki"


class Saldo(models.Model):
    data = models.DateTimeField(default=datetime.now, blank=True)
    kwota = models.DecimalField(max_digits=9999999, decimal_places=2)

    class Meta:
        verbose_name = "Saldo"
        verbose_name_plural = "Saldo"
