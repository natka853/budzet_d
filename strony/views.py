from django.shortcuts import render
from Budzet.models import Dochod


# Create your views here.
def home_view(request, *args, **kwargs):
    #  return HttpResponse("<h1>Budżet domowy</h1>")
    return render(request, "home.html", {})


def dochody(request, *args, **kwargs):
    incomes = Dochod.objects.all() #zbiór wszystkich dochodów z bazy
    return render(request, "dochody.html", {'incomes': incomes})


def wydatki(request, *args, **kwargs):
    return render(request, "wydatki.html", {})


def podsumowanie(request, *args, **kwargs):
    return render(request, "podsumowanie.html", {})


def dodajWydatek(request, *args, **kwargs):
    return render(request, "dodajWydatek.html", {})


def dodajPrzychod(request, *args, **kwargs):
    return render(request, "dodajPrzychod.html", {})


def dodajKategorieWydatku(request, *args, **kwargs):
    return render(request, "dodajKategorieWydatku.html", {})


def dodajZrodloDochodu(request, *args, **kwargs):
    return render(request, "dodajZrodloDochodu.html", {})
