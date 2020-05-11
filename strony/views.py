from django.shortcuts import render
from Budzet.models import Dochod
from Budzet.models import Wydatek
from Budzet.models import Zrodlo
from Budzet.models import Kategoria
from Budzet.forms import ZrodloForm
from Budzet.forms import KategoriaForm
from Budzet.forms import DochodForm


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


def dodaj_wydatek(request, *args, **kwargs):
    categories = Kategoria.objects.all()
    return render(request, "dodajWydatek.html", {'categories': categories})


def dodaj_przychod(request, *args, **kwargs): #TODO pobieranie od użytkownika
    sources = Zrodlo.objects.all()
    form = DochodForm(request.POST or None)
    if form.is_valid():
        form.save(commit=True)  # zapis do bazy danych
        form = DochodForm()  # odświeżanie formularza
    return render(request, "dodajPrzychod.html", {'sources': sources, 'form': form})


def dodaj_kategorie_wydatku(request, *args, **kwargs):
    form = KategoriaForm(request.POST or None)
    if form.is_valid():
        form.save(commit=True)  # zapis do bazy danych
        form = KategoriaForm()  # odświeżanie formularza
    return render(request, "dodajKategorieWydatku.html", {'form': form})


def dodaj_zrodlo_dochodu(request, *args, **kwargs):
    form = ZrodloForm(request.POST or None)
    if form.is_valid():
        form.save(commit=True) #zapis do bazy danych
        form = ZrodloForm() #odświeżanie formularza
    return render(request, "dodajZrodloDochodu.html", {'form': form})


def logowanie(request, *args, **kwargs):
    return render(request, "logowanie.html", {})


def rejestrowanie(request, *args, **kwargs):
    return render(request, "rejestrowanie.html", {})
