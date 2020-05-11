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

from strony.views import home_view, dochody, wydatki, podsumowanie, dodajWydatek, dodajPrzychod, dodajKategorieWydatku, dodajZrodloDochodu, logowanie, rejestrowanie


urlpatterns = [
    path('', home_view, name='home'),
    path('podsumowanie/', podsumowanie),
    path('dochody/', dochody),
    path('wydatki/', wydatki),
    path('dodajWydatek/', dodajWydatek),
    path('dodajPrzychod/', dodajPrzychod),
    path('dodajKategorieWydatku/', dodajKategorieWydatku),
    path('dodajZrodloDochodu/', dodajZrodloDochodu),
    path('logowanie/', logowanie),
    path('rejestrowanie/', rejestrowanie),
    path('admin/', admin.site.urls),
]
