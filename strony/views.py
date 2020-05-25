from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from Budzet.models import Dochod
from Budzet.models import Wydatek
from Budzet.models import Zrodlo
from Budzet.models import Kategoria
from Budzet.forms import ZrodloForm
from Budzet.forms import KategoriaForm
from Budzet.forms import DochodForm
from Budzet.forms import WydatekForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegisterForm


def home_view(request, *args, **kwargs):
    username = ""
    if request.user.is_authenticated:
        username = request.user.username  # logged user's username
    return render(request, "home.html", {'username': username})


def dochody(request, *args, **kwargs):
    if request.user.is_authenticated:
        incomes = Dochod.objects.filter(zrodlo__in=Zrodlo.objects.filter(user=request.user.id))
        return render(request, "dochody.html", {'incomes': incomes})
    else:
        return render(request, "unlogged.html", {})


def wydatki(request, *args, **kwargs):
    if request.user.is_authenticated:
        expenses = Wydatek.objects.filter(kategoria__in=Kategoria.objects.filter(user=request.user.id))
        return render(request, "wydatki.html", {'expenses': expenses})
    else:
        return render(request, "unlogged.html", {})


def podsumowanie(request, *args, **kwargs):
    if request.user.is_authenticated:
        incomes = Dochod.objects.filter(zrodlo__in=Zrodlo.objects.filter(user=request.user.id))
        expenses = Wydatek.objects.filter(kategoria__in=Kategoria.objects.filter(user=request.user.id))
        return render(request, "podsumowanie.html", {'incomes': incomes, 'expenses': expenses})
    else:
        return render(request, "unlogged.html", {})


def zrodla(request, *args, **kwargs):
    if request.user.is_authenticated:
        sources = Zrodlo.objects.filter(user=request.user.id)
        return render(request, "zrodla.html", {'sources': sources})
    else:
        return render(request, "unlogged.html", {})


def kategorie(request, *args, **kwargs):
    if request.user.is_authenticated:
        categories = Kategoria.objects.filter(user=request.user.id)
        return render(request, "kategorie.html", {'categories': categories})
    else:
        return render(request, "unlogged.html", {})


def dodaj_wydatek(request, *args, **kwargs):
    if request.user.is_authenticated:
        categories = Kategoria.objects.filter(user=request.user.id)
        form = WydatekForm(request.POST or None)
        print(form.errors)
        if form.is_valid():
            form.save(commit=True)  # zapis do bazy danych
            form = WydatekForm()  # odświeżanie formularza
        return render(request, "dodajWydatek.html", {'categories': categories, 'form': form})
    else:
        return render(request, "unlogged.html", {})


def dodaj_przychod(request, *args, **kwargs):
    if request.user.is_authenticated:
        sources = Zrodlo.objects.filter(user=request.user.id)
        form = DochodForm(request.POST or None)
        print(form.errors)
        if form.is_valid():
            form.save(commit=True)  # zapis do bazy danych
            form = DochodForm()  # odświeżanie formularza
        return render(request, "dodajPrzychod.html", {'sources': sources, 'form': form})
    else:
        return render(request, "unlogged.html", {})


def dodaj_kategorie_wydatku(request, *args, **kwargs):
    if request.user.is_authenticated:
        form = KategoriaForm(request.POST or None)
        if form.is_valid():
            us = form.save(commit=False)  # zapis obiektu
            us.user = request.user  # ustawienie użytkownika na zalogowanego
            us.save()  # zapis do bazy
            form = KategoriaForm()  # odświeżanie formularza
        return render(request, "dodajKategorieWydatku.html", {'form': form})
    else:
        return render(request, "unlogged.html", {})


def dodaj_zrodlo_dochodu(request, *args, **kwargs):
    if request.user.is_authenticated:
        form = ZrodloForm(request.POST or None)
        if form.is_valid():
            us = form.save(commit=False)  # zapis obiektu
            us.user = request.user  # ustawienie użytkownika na zalogowanego
            us.save()
            form = ZrodloForm()  # odświeżanie formularza
        return render(request, "dodajZrodloDochodu.html", {'form': form})
    else:
        return render(request, "unlogged.html", {})


def edytuj_kategorie_wydatku(request, *args, **kwargs):
    if request.user.is_authenticated:
        form = KategoriaForm(request.POST or None)
        if form.is_valid():
            us = form.save(commit=False)  # zapis obiektu
            us.user = request.user  # ustawienie użytkownika na zalogowanego
            # TODO
        return render(request, "edytujKategorieWydatku.html", {'form': form})
    else:
        return render(request, "unlogged.html", {})


def edytuj_zrodlo_dochodu(request, *args, **kwargs):
    if request.user.is_authenticated:
        form = ZrodloForm(request.POST or None)
        if form.is_valid():
            us = form.save(commit=False)  # zapis obiektu
            us.user = request.user  # ustawienie użytkownika na zalogowanego
            # TODO
        return render(request, "edytujZrodloDochodu.html", {'form': form})
    else:
        return render(request, "unlogged.html", {})


def logowanie(request, *args, **kwargs):
    return render(request, "logowanie.html", {})


def rejestrowanie(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save(commit=True)
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, "rejestrowanie.html", {'form': form})


def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/")


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            ###W TYM MIEJSCU MOZNA COS TAM POROBIC
            ###U NAS NP. PO REJESTRACJI TWORZYMY NOWEGO UZYTKOWNIKOWI FOLDER NA SERWERZE
            ###UZYWAJAC WPISANEGO USERNAME'A
            # username = form.cleaned_data.get('username')
            # user = User.objects.filter(username=username).first()
            # directory = Directory(directoryName = username + "_root", owner = user)
            # disk = Disk(mainDirectory = directory, owner = user, maxSize = 31457280)
            # os.mkdir( settings.MEDIA_ROOT + "\\" + directory.directoryName)
            # directory.save()
            # disk.save()
            return redirect('home')  # powrot do strony glownej
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
