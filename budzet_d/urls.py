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

from Budzet.views import home_view, dochody, wydatki, podsumowanie, dodaj_wydatek, dodaj_przychod, \
    dodaj_kategorie_wydatku, dodaj_zrodlo_dochodu, logowanie, rejestrowanie, zrodla, kategorie, edytuj_zrodlo_dochodu, \
    edytuj_kategorie_wydatku, register, register_success, edit_income, edit_expense, delete_expense, delete_income, \
    delete_category, delete_source, delete_account

urlpatterns = [
    path('', home_view, name='home'),
    path('podsumowanie/', podsumowanie),
    path('dochody/', dochody),
    path('wydatki/', wydatki),
    path('zrodla/', zrodla),
    path('kategorie/', kategorie),
    path('dodajWydatek/', dodaj_wydatek),
    path('dodajPrzychod/', dodaj_przychod),
    path('dodajKategorieWydatku/', dodaj_kategorie_wydatku),
    path('<int:nr>/edytujKategorieWydatku/', edytuj_kategorie_wydatku),
    path('dodajZrodloDochodu/', dodaj_zrodlo_dochodu),
    path('<int:nr>/edytujZrodloDochodu/', edytuj_zrodlo_dochodu),
    path('logowanie/', logowanie),
    path('rejestrowanie/', rejestrowanie),
    path('admin/', admin.site.urls),
    path('<int:nr>/edytujDochod/', edit_income),
    path('<int:nr>/edytujWydatek/', edit_expense),
    path('<int:nr>/usunietoWydatek/', delete_expense),
    path('<int:nr>/usunietoDochod/', delete_income),
    path('<int:nr>/usunietoKategorie/', delete_category),
    path('<int:nr>/usunietoZrodlo/', delete_source),
    path('usunietoKonto/', delete_account),
    # path('logout/', logout_page),
    path('register/', register),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('accounts/profile/', home_view),
    # path('register_success/', TemplateView.as_view(template_name='users/register_success.html'),
    # name='register_success'),
    path('register_success/', register_success)  # to nie wiem czy jest dobrze - możliwe do zmiany
]
