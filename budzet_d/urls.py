"""untitled8 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from Budzet.views import home_view, my_incomes, my_expenses, summary, add_income, add_expense, \
    add_expense_category, add_income_source, my_sources, my_categories, edit_income_source, \
    edit_expense_category, register, edit_income, edit_expense, delete_expense, delete_income, \
    delete_category, delete_source, delete_account, err404

urlpatterns = [
    path('', home_view, name='home'),
    path('podsumowanie/', summary),
    path('dochody/', my_incomes),
    path('wydatki/', my_expenses),
    path('zrodla/', my_sources),
    path('kategorie/', my_categories),
    path('dodajWydatek/', add_income),
    path('dodajPrzychod/', add_expense),
    path('dodajKategorieWydatku/', add_expense_category),
    path('<int:nr>/edytujKategorieWydatku/', edit_expense_category),
    path('dodajZrodloDochodu/', add_income_source),
    path('<int:nr>/edytujZrodloDochodu/', edit_income_source),
    path('admin/', admin.site.urls),
    path('<int:nr>/edytujDochod/', edit_income),
    path('<int:nr>/edytujWydatek/', edit_expense),
    path('<int:nr>/usunietoWydatek/', delete_expense),
    path('<int:nr>/usunietoDochod/', delete_income),
    path('<int:nr>/usunietoKategorie/', delete_category),
    path('<int:nr>/usunietoZrodlo/', delete_source),
    path('usunietoKonto/', delete_account),
    path('register/', register),
    path('err404/', err404),  # Tymczasowo do podglądu strony błędu
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('accounts/profile/', home_view),
]
