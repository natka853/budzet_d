from django.db import models

# Create your models here.
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

    class Meta:
        verbose_name = "Wydatek"
        verbose_name_plural = "Wydatki"

