from django.contrib.auth import authenticate, login
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.utils.datetime_safe import datetime

from Budzet.models import Dochod
from Budzet.models import Wydatek
from Budzet.models import Zrodlo
from Budzet.models import Kategoria
from Budzet.forms import ZrodloForm, EditCategoryForm
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


# to do poprawy(ale jeszcze nie rozkminiłam)
def register_success(request, *args, **kwargs):
    return render(request, "users/register_success.html", {})


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
        incomes_sum = Dochod.objects.filter(zrodlo__user=request.user.id).aggregate(Sum('kwota'))
        if incomes_sum['kwota__sum'] is None:
            incomes_sum['kwota__sum'] = '0.00'
        expenses_sum = Wydatek.objects.filter(kategoria__user=request.user.id).aggregate(Sum('kwota'))
        if expenses_sum['kwota__sum'] is None:
            expenses_sum['kwota__sum'] = '0.00'
        saldo = round(incomes_sum['kwota__sum'] - expenses_sum['kwota__sum'], 2)
        today = datetime.today()
        today_incomes = Dochod.objects.filter(zrodlo__user=request.user.id, data__year=today.year,
                                              data__month=today.month, data__day=today.day).aggregate(Sum('kwota'))
        if today_incomes['kwota__sum'] is None:
            today_incomes['kwota__sum'] = '0.00'
        else:
            today_incomes['kwota__sum'] = round(today_incomes['kwota__sum'], 2)
        today_expenses = Wydatek.objects.filter(kategoria__user=request.user.id, data__year=today.year,
                                                data__month=today.month, data__day=today.day).aggregate(Sum('kwota'))
        if today_expenses['kwota__sum'] is None:
            today_expenses['kwota__sum'] = '0.00'
        else:
            today_expenses['kwota__sum'] = round(today_expenses['kwota__sum'], 2)
        return render(request, "podsumowanie.html", {'incomes': incomes, 'expenses': expenses,
                                                     'saldo': saldo, 'today_incomes': today_incomes['kwota__sum'],
                                                     'today_expenses': today_expenses['kwota__sum'], 'today': today})
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
        form = EditCategoryForm(request.POST or None)
        categories = Kategoria.objects.filter(user=request.user.id)
        if form.is_valid():
            us = form.save(commit=False)  # zapis obiektu
            us.user = request.user  # ustawienie użytkownika na zalogowanego #TODO
            nazwa = form.cleaned_data.get('nazwa')
            category = Kategoria.objects.get(user=request.user.id, nazwa=nazwa)
            name = form.cleaned_data.get('name')
            category.nazwa = name
            us.save(commit=True)
            form.EditCategoryForm()
        return render(request, "edytujKategorieWydatku.html", {'form': form, 'categories': categories})
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


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
