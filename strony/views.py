from django.shortcuts import render
from Budzet.models import Dochod
from Budzet.models import Wydatek
from Budzet.models import Zrodlo
from Budzet.models import Kategoria


# Create your views here.
def home_view(request, *args, **kwargs):
    #  return HttpResponse("<h1>Budżet domowy</h1>")
    return render(request, "home.html", {})


def dochody(request, *args, **kwargs):
    incomes = Dochod.objects.all()  # zbiór wszystkich dochodów z bazy
    return render(request, "dochody.html", {'incomes': incomes})


def wydatki(request, *args, **kwargs):
    expenses = Wydatek.objects.all()  # zbiór wszystkich wydatków z bazy
    return render(request, "wydatki.html", {'expenses': expenses})


def podsumowanie(request, *args, **kwargs):
    incomes = Dochod.objects.all()  # zbiór wszystkich dochodów z bazy
    expenses = Wydatek.objects.all()  # zbiór wszystkich wydatków z bazy
    return render(request, "podsumowanie.html", {'incomes': incomes, 'expenses': expenses})


def dodajWydatek(request, *args, **kwargs):
    categories = Kategoria.objects.all()
    return render(request, "dodajWydatek.html", {'categories': categories})


def dodajPrzychod(request, *args, **kwargs):
    sources = Zrodlo.objects.all()
    return render(request, "dodajPrzychod.html", {'sources': sources})


def dodajKategorieWydatku(request, *args, **kwargs):
    return render(request, "dodajKategorieWydatku.html", {})


def dodajZrodloDochodu(request, *args, **kwargs):
    return render(request, "dodajZrodloDochodu.html", {})


def logowanie(request, *args, **kwargs):
    return render(request, "logowanie.html", {})


def rejestrowanie(request, *args, **kwargs):
    return render(request, "rejestrowanie.html", {})
