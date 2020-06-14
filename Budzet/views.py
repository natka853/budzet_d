import plotly
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import date, timedelta
import plotly.graph_objects as go
# import plotly.express as px

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from Budzet.models import Dochod, Wydatek, Zrodlo, Kategoria
from Budzet.forms import SourceForm, EditSourceForm, EditIncomeForm, EditExpenseForm, EditCategoryForm, \
    AdminRegisterForm
from Budzet.forms import CategoryForm, IncomeForm, ExpenseForm
from django.shortcuts import render, get_object_or_404, redirect  # , redirect
from .forms import UserRegisterForm


def err404(request, *args, **kwargs):  # tymczasowo do podglądu strony błędu
    return render(request, "404.html", {})


def home_view(request, *args, **kwargs):
    username = ""
    if request.user.is_authenticated:
        username = request.user.username  # logged user's username
    return render(request, "home.html", {'username': username})


def my_incomes(request, *args, **kwargs):
    if request.user.is_authenticated:
        incomes = Dochod.objects.filter(zrodlo__in=Zrodlo.objects.filter(user=request.user.id))
        return render(request, "dochody.html", {'incomes': incomes})
    else:
        return render(request, "unlogged.html", {})


def my_expenses(request, *args, **kwargs):
    if request.user.is_authenticated:
        expenses = Wydatek.objects.filter(kategoria__in=Kategoria.objects.filter(user=request.user.id))
        return render(request, "wydatki.html", {'expenses': expenses})
    else:
        return render(request, "unlogged.html", {})


def summary(request, *args, **kwargs):
    if request.user.is_authenticated:
        act_date = date.today() - timedelta(days=30)
        dates = [act_date.strftime('%d-%m-%Y'), ]
        incomes_balance = Dochod.objects.filter(zrodlo__user=request.user.id, data__lte=act_date).aggregate(
            Sum('kwota'))
        if incomes_balance['kwota__sum'] is None:
            incomes_balance['kwota__sum'] = 0.00
        expenses_balance = Wydatek.objects.filter(kategoria__user=request.user.id, data__lte=act_date).aggregate(
            Sum('kwota'))
        if expenses_balance['kwota__sum'] is None:
            expenses_balance['kwota__sum'] = 0.00
        bal = round(float(incomes_balance['kwota__sum']) - float(expenses_balance['kwota__sum']), 2)
        daily_balance = [bal, ]
        act_date += timedelta(days=1)
        while act_date <= date.today():
            dates.append(act_date.strftime('%d-%m-%Y'))
            incomes_balance = Dochod.objects.filter(zrodlo__user=request.user.id, data=act_date).aggregate(
                Sum('kwota'))
            if incomes_balance['kwota__sum'] is None:
                incomes_balance['kwota__sum'] = 0.00
            expenses_balance = Wydatek.objects.filter(kategoria__user=request.user.id, data=act_date).aggregate(
                Sum('kwota'))
            if expenses_balance['kwota__sum'] is None:
                expenses_balance['kwota__sum'] = 0.00
            bal += round(float(incomes_balance['kwota__sum']) - float(expenses_balance['kwota__sum']), 2)
            act_date += timedelta(days=1)
            daily_balance.append(bal)
        fig = go.Figure(go.Scatter(
            x=dates,
            y=daily_balance,
            mode='lines+markers'
        ))
        fig.update_layout(
            xaxis=dict(
                tickmode='linear',
                tick0=0.5,
                dtick=0.75,
                title='Data',
                titlefont={'family': 'Times New Roman'}
            ),
            yaxis=dict(title='Saldo', titlefont={'family': 'Times New Roman'}),
            title={'text': 'Twoje saldo z ostatnich 30 dni', 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
            titlefont={'family': 'Times New Roman'},
            paper_bgcolor='ghostwhite'
        )
        graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")

        labels_cat = []
        values_cat = []
        for category in Kategoria.objects.filter(user=request.user.id):
            labels_cat.append(category.nazwa)
            values_cat.append(Wydatek.objects.filter(kategoria=category).aggregate(Sum('kwota'))['kwota__sum'])
        fig_cat = go.Figure(data=[go.Pie(labels=labels_cat, values=values_cat)])
        fig_cat.update_layout(
            title={'text': 'Udział kategorii wydatków', 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
            titlefont={'family': 'Times New Roman'},
            paper_bgcolor='ghostwhite'
        )
        graph_div_cat = plotly.offline.plot(fig_cat, auto_open=False, output_type="div")

        labels_src = []
        values_src = []
        for source in Zrodlo.objects.filter(user=request.user.id):
            labels_src.append(source.nazwa)
            values_src.append(Dochod.objects.filter(zrodlo=source).aggregate(Sum('kwota'))['kwota__sum'])
        fig_src = go.Figure(data=[go.Pie(labels=labels_src, values=values_src)])
        fig_src.update_layout(
            title={'text': 'Udział źródeł dochodów', 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
            titlefont={'family': 'Times New Roman'},
            paper_bgcolor='ghostwhite'
        )
        graph_div_src = plotly.offline.plot(fig_src, auto_open=False, output_type="div")

        incomes = Dochod.objects.filter(zrodlo__in=Zrodlo.objects.filter(user=request.user.id)).order_by('data')
        expenses = Wydatek.objects.filter(kategoria__in=Kategoria.objects.filter(user=request.user.id)).order_by('data')
        incomes_sum = Dochod.objects.filter(zrodlo__user=request.user.id).aggregate(Sum('kwota'))
        if incomes_sum['kwota__sum'] is None:
            incomes_sum['kwota__sum'] = 0.00
        expenses_sum = Wydatek.objects.filter(kategoria__user=request.user.id).aggregate(Sum('kwota'))
        if expenses_sum['kwota__sum'] is None:
            expenses_sum['kwota__sum'] = 0.00
        balance = round(float(incomes_sum['kwota__sum']) - float(expenses_sum['kwota__sum']), 2)
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
                                                     'balance': balance, 'today_incomes': today_incomes['kwota__sum'],
                                                     'today_expenses': today_expenses['kwota__sum'], 'fig': graph_div,
                                                     'fig2': graph_div_cat, 'fig3': graph_div_src})
    else:
        return render(request, "unlogged.html", {})


def my_sources(request, *args, **kwargs):
    if request.user.is_authenticated:
        sources = Zrodlo.objects.filter(user=request.user.id)
        return render(request, "zrodla.html", {'sources': sources})
    else:
        return render(request, "unlogged.html", {})


def my_categories(request, *args, **kwargs):
    if request.user.is_authenticated:
        categories = Kategoria.objects.filter(user=request.user.id)
        return render(request, "kategorie.html", {'categories': categories})
    else:
        return render(request, "unlogged.html", {})


def add_income(request, *args, **kwargs):
    if request.user.is_authenticated:
        categories = Kategoria.objects.filter(user=request.user.id)
        today = date.today()
        form = ExpenseForm(request.POST or None)
        print(form.errors)
        if form.is_valid():
            expense = form.save(commit=False)
            if not request.POST['data']:
                expense.data = today
            expense.save()  # zapis do bazy danych
            form = ExpenseForm()  # odświeżanie formularza
            messages.success(request, 'Dodano wydatek')
        return render(request, "dodajWydatek.html", {'categories': categories, 'form': form})
    else:
        return render(request, "unlogged.html", {})


def add_expense(request, *args, **kwargs):
    if request.user.is_authenticated:
        sources = Zrodlo.objects.filter(user=request.user.id)
        today = date.today()
        form = IncomeForm(request.POST or None)
        print(form.errors)
        if form.is_valid():
            income = form.save(commit=False)
            if not request.POST['data']:
                income.data = today
            income.save()  # zapis do bazy danych
            form = IncomeForm()  # odświeżanie formularza
            messages.success(request, 'Dodano dochód')
        return render(request, "dodajPrzychod.html", {'sources': sources, 'form': form})
    else:
        return render(request, "unlogged.html", {})


def add_expense_category(request, *args, **kwargs):
    if request.user.is_authenticated:
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            us = form.save(commit=False)  # zapis obiektu
            us.user = request.user  # ustawienie użytkownika na zalogowanego
            us.save()  # zapis do bazy
            form = CategoryForm()  # odświeżanie formularza
            messages.success(request, 'Dodano kategorię')
        return render(request, "dodajKategorieWydatku.html", {'form': form})
    else:
        return render(request, "unlogged.html", {})


def add_income_source(request, *args, **kwargs):
    if request.user.is_authenticated:
        form = SourceForm(request.POST or None)
        if form.is_valid():
            us = form.save(commit=False)  # zapis obiektu
            us.user = request.user  # ustawienie użytkownika na zalogowanego
            us.save()
            form = SourceForm()  # odświeżanie formularza
            messages.success(request, 'Dodano źródło')
        return render(request, "dodajZrodloDochodu.html", {'form': form})
    else:
        return render(request, "unlogged.html", {})


def edit_expense_category(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        form = EditCategoryForm(request.POST or None)
        category = get_object_or_404(Kategoria, id=nr)
        if category.user.id != request.user.id:
            return render(request, "noPermission.html", {})
        if form.is_valid():
            category.nazwa = form.cleaned_data.get('nazwa')
            category.save()
            form = EditCategoryForm()
        return render(request, "edytujKategorieWydatku.html", {'form': form, 'category': category})
    else:
        return render(request, "unlogged.html", {})


def edit_income_source(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        form = EditSourceForm(request.POST or None)
        source = get_object_or_404(Zrodlo, id=nr)
        if source.user.id != request.user.id:
            return render(request, "noPermission.html", {})
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
        income = get_object_or_404(Dochod, id=nr)
        if income.zrodlo.user.id != request.user.id:
            return render(request, "noPermission.html", {})
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
        expense = get_object_or_404(Wydatek, id=nr)
        if expense.kategoria.user.id != request.user.id:
            return render(request, "noPermission.html", {})
        expense.delete()
        return render(request, "usunietoWydatek.html", {})
    else:
        return render(request, "unlogged.html", {})


def delete_income(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        income = get_object_or_404(Dochod, id=nr)
        if income.zrodlo.user.id != request.user.id:
            return render(request, "noPermission.html", {})
        income.delete()
        return render(request, "usunietoDochod.html", {})
    else:
        return render(request, "unlogged.html", {})


def delete_category(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        category = get_object_or_404(Kategoria, id=nr)
        if category.user.id != request.user.id:
            return render(request, "noPermission.html", {})
        category.delete()
        return render(request, "usunietoKategorie.html", {})
    else:
        return render(request, "unlogged.html", {})


def delete_source(request, nr, *args, **kwargs):
    if request.user.is_authenticated:
        source = get_object_or_404(Zrodlo, id=nr)
        if source.user.id != request.user.id:
            return render(request, "noPermission.html", {})
        source.delete()
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
        expense = get_object_or_404(Wydatek, id=nr)
        if expense.kategoria.user.id != request.user.id:
            return render(request, "noPermission.html", {})
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


def register_admin(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return render(request, 'users/admin_register_success.html', {})
    else:
        form = AdminRegisterForm()
    return render(request, 'users/admin_register.html', {'form': form})


def is_valid_queryparam(param):
    return param != '' and param is not None


def FilterExpenses(request):
    wy = Wydatek.objects.filter(kategoria__user=request.user.id)
    categories = Kategoria.objects.filter(user=request.user.id)

    name_contains_query = request.GET.get('name_contains')
    id_exact_query = request.GET.get('id_exact')
    description_contains_query = request.GET.get('description_contains')
    kwota_min = request.GET.get('kwota_min')
    kwota_max = request.GET.get('kwota_max')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    category = request.GET.get('category')

    if is_valid_queryparam(name_contains_query):
        wy = wy.filter(nazwa__icontains=name_contains_query)

    if is_valid_queryparam(id_exact_query):
        wy = wy.filter(id=id_exact_query)

    if is_valid_queryparam(description_contains_query):
        wy = wy.filter(opis__icontains=description_contains_query)

    if is_valid_queryparam(kwota_min):
        wy = wy.filter(kwota__gte=kwota_min)

    if is_valid_queryparam(kwota_max):
        wy = wy.filter(kwota__lt=kwota_max)

    if is_valid_queryparam(date_min):
        wy = wy.filter(data__gte=date_min)

    if is_valid_queryparam(date_max):
        wy = wy.filter(data__lt=date_max)

    if is_valid_queryparam(category) & (category != "Wybierz..."):
        wy = wy.filter(kategoria__nazwa=category)

    context = {
        'queryset': wy,
        'categories': categories,
    }

    return render(request, "filtrujWydatki.html", context)


def FilterIncomes(request):
    if request.user.is_authenticated:
        do = Dochod.objects.filter(zrodlo__user=request.user.id)
        sources = Zrodlo.objects.filter(user=request.user.id)

        name_contains_query = request.GET.get('name_contains')
        id_exact_query = request.GET.get('id_exact')
        description_contains_query = request.GET.get('description_contains')
        kwota_min = request.GET.get('kwota_min')
        kwota_max = request.GET.get('kwota_max')
        date_min = request.GET.get('date_min')
        date_max = request.GET.get('date_max')
        zrodlo = request.GET.get('zrodlo')

        if is_valid_queryparam(name_contains_query):
            do = do.filter(nazwa__icontains=name_contains_query)

        if is_valid_queryparam(id_exact_query):
            do = do.filter(id=id_exact_query)

        if is_valid_queryparam(description_contains_query):
            do = do.filter(opis__icontains=description_contains_query)

        if is_valid_queryparam(kwota_min):
            do = do.filter(kwota__gte=kwota_min)

        if is_valid_queryparam(kwota_max):
            do = do.filter(kwota__lt=kwota_max)

        if is_valid_queryparam(date_min):
            do = do.filter(data__gte=date_min)

        if is_valid_queryparam(date_max):
            do = do.filter(data__lt=date_max)

        if is_valid_queryparam(zrodlo) & (zrodlo != "Wybierz..."):
            do = do.filter(zrodlo__nazwa=zrodlo)

        context = {
            'queryset': do,
            'sources': sources,
        }

        return render(request, "filtrujDochod.html", context)
    else:
        return render(request, "unlogged.html", {})


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            incomes = Dochod.objects.filter(zrodlo__in=Zrodlo.objects.filter(user=request.user.id)).order_by('data')
            expenses = Wydatek.objects.filter(kategoria__in=Kategoria.objects.filter(user=request.user.id)).order_by(
                'data')
            pdf = render_to_pdf('app/pdf_template.html', {'incomes': incomes, 'expenses': expenses})
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            return render(request, "unlogged.html", {})


class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            incomes = Dochod.objects.filter(zrodlo__in=Zrodlo.objects.filter(user=request.user.id)).order_by('data')
            expenses = Wydatek.objects.filter(kategoria__in=Kategoria.objects.filter(user=request.user.id)).order_by(
                'data')
            pdf = render_to_pdf('app/pdf_template.html', {'incomes': incomes, 'expenses': expenses})

            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Transakcje_%s.pdf" % ("1")
            content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        else:
            return render(request, "unlogged.html", {})
