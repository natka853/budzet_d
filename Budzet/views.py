from datetime import date
import time

from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render

from Budzet.forms import DochodForm
from Budzet.forms import KategoriaForm
from Budzet.forms import WydatekForm
from Budzet.forms import ZrodloForm, EditSourceForm, EditIncomeForm, EditExpenseForm, EditCategoryForm
from Budzet.models import Dochod
from Budzet.models import Kategoria
from Budzet.models import Wydatek
from Budzet.models import Zrodlo
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
        '''fig = go.Figure(go.Scatter(
            x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            y=[28.8, 28.5, 37, 56.8, 69.7, 79.7, 78.5, 77.8, 74.1, 62.6, 45.3, 39.9]
        ))

        fig.update_layout(
            xaxis=dict(
                tickmode='linear',
                tick0=0.5,
                dtick=0.75
            )
        )
        fig.show()'''  # po odkomentowaniu pokaże tylko wykres a nie podsumowanie
        incomes = Dochod.objects.filter(zrodlo__in=Zrodlo.objects.filter(user=request.user.id))
        expenses = Wydatek.objects.filter(kategoria__in=Kategoria.objects.filter(user=request.user.id))
        incomes_sum = Dochod.objects.filter(zrodlo__user=request.user.id).aggregate(Sum('kwota'))
        if incomes_sum['kwota__sum'] is None:
            incomes_sum['kwota__sum'] = 0.00
        expenses_sum = Wydatek.objects.filter(kategoria__user=request.user.id).aggregate(Sum('kwota'))
        if expenses_sum['kwota__sum'] is None:
            expenses_sum['kwota__sum'] = 0.00
        saldo = round(float(incomes_sum['kwota__sum']) - float(expenses_sum['kwota__sum']), 2)
        today = date.today()
        today_incomes = Dochod.objects.filter(zrodlo__user=request.user.id, data=today).aggregate(Sum('kwota'))
        if today_incomes['kwota__sum'] is None:
            today_incomes['kwota__sum'] = '0.00'
        else:
            today_incomes['kwota__sum'] = round(today_incomes['kwota__sum'], 2)
        today_expenses = Wydatek.objects.filter(kategoria__user=request.user.id, data=today).aggregate(Sum('kwota'))
        if today_expenses['kwota__sum'] is None:
            today_expenses['kwota__sum'] = '0.00'
        else:
            today_expenses['kwota__sum'] = round(today_expenses['kwota__sum'], 2)
        return render(request, "podsumowanie.html", {'incomes': incomes, 'expenses': expenses,
                                                     'saldo': saldo, 'today_incomes': today_incomes['kwota__sum'],
                                                     'today_expenses': today_expenses['kwota__sum']})
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
        today = date.today()
        form = WydatekForm(request.POST or None)
        print(form.errors)
        if form.is_valid():
            expense = form.save(commit=False)
            if not request.POST['data']:
                expense.data = today
            expense.save()  # zapis do bazy danych
            form = WydatekForm()  # odświeżanie formularza
            time.sleep(4)
        return render(request, "dodajWydatek.html", {'categories': categories, 'form': form})
    else:
        return render(request, "unlogged.html", {})


def dodaj_przychod(request, *args, **kwargs):
    if request.user.is_authenticated:
        sources = Zrodlo.objects.filter(user=request.user.id)
        today = date.today()
        form = DochodForm(request.POST or None)
        print(form.errors)
        if form.is_valid():
            income = form.save(commit=False)
            if not request.POST['data']:
                income.data = today
            income.save()  # zapis do bazy danych
            form = DochodForm()  # odświeżanie formularza
            time.sleep(4)
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
            time.sleep(4)
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
            time.sleep(4)
        return render(request, "dodajZrodloDochodu.html", {'form': form})
    else:
        return render(request, "unlogged.html", {})


def edytuj_kategorie_wydatku(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        form = EditCategoryForm(request.POST or None)
        category = Kategoria.objects.get(id=nr)
        if form.is_valid():
            category.nazwa = form.cleaned_data.get('nazwa')
            category.save()
            form = EditCategoryForm()
        return render(request, "edytujKategorieWydatku.html", {'form': form, 'category': category})
    else:
        return render(request, "unlogged.html", {})


def edytuj_zrodlo_dochodu(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        form = EditSourceForm(request.POST or None)
        source = Zrodlo.objects.get(id=nr)
        if form.is_valid():
            source.nazwa = form.cleaned_data.get('nazwa')
            source.save()
            form = EditSourceForm()
        return render(request, "edytujZrodloDochodu.html", {'form': form, 'source': source})
    else:
        return render(request, "unlogged.html", {})


def edit_income(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        form = EditIncomeForm(request.POST or None)
        income = Dochod.objects.get(id=nr)
        sources = Zrodlo.objects.filter(user=request.user.id).exclude(id=income.zrodlo.id)
        if form.is_valid():
            if request.POST['nazwa']:
                income.nazwa = form.cleaned_data.get('nazwa')
            if request.POST['opis']:
                income.opis = form.cleaned_data.get('opis')
            if request.POST['kwota']:
                income.kwota = form.cleaned_data.get('kwota')
            if request.POST['data']:
                income.data = form.cleaned_data.get('data')
            income.zrodlo = form.cleaned_data.get('zrodlo')
            income.save()
            form = EditIncomeForm()
        return render(request, "edytujDochod.html", {'form': form, 'sources': sources, 'income': income})
    else:
        return render(request, "unlogged.html", {})


def delete_expense(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        Wydatek.objects.get(id=nr).delete()
        return render(request, "usunietoWydatek.html", {})
    else:
        return render(request, "unlogged.html", {})


def delete_income(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        Dochod.objects.get(id=nr).delete()
        return render(request, "usunietoDochod.html", {})
    else:
        return render(request, "unlogged.html", {})


def delete_category(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        Kategoria.objects.get(id=nr).delete()
        return render(request, "usunietoKategorie.html", {})
    else:
        return render(request, "unlogged.html", {})


def delete_source(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        Zrodlo.objects.get(id=nr).delete()
        return render(request, "usunietoKategorie.html", {})
    else:
        return render(request, "unlogged.html", {})


def delete_account(request, *args, **kwargs):
    if request.user.is_authenticated:
        User.objects.get(id=request.user.id).delete()
        return render(request, "usunKonto.html", {})
    else:
        return render(request, "unlogged.html", {})


def edit_expense(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        form = EditExpenseForm(request.POST or None)
        expense = Wydatek.objects.get(id=nr)
        categories = Kategoria.objects.filter(user=request.user.id).exclude(id=expense.kategoria.id)
        if form.is_valid():
            if request.POST['nazwa']:
                expense.nazwa = form.cleaned_data.get('nazwa')
            if request.POST['opis']:
                expense.opis = form.cleaned_data.get('opis')
            if request.POST['kwota']:
                expense.kwota = form.cleaned_data.get('kwota')
            if request.POST['data']:
                expense.data = form.cleaned_data.get('data')
            expense.kategoria = form.cleaned_data.get('kategoria')
            expense.save()
            form = EditExpenseForm()
        return render(request, "edytujWydatek.html", {'form': form, 'categories': categories, 'expense': expense})
    else:
        return render(request, "unlogged.html", {})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return render(request, 'users/register_success.html', {})
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
