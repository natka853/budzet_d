from django.shortcuts import render


# Create your views here.
def home_view(request, *args, **kwargs):
    #  return HttpResponse("<h1>Budżet domowy</h1>")
    return render(request, "home.html", {})


def dochody(request, *args, **kwargs):
    # return HttpResponse("<h1>Tu są twoje dochody</h1>")
    return render(request, "dochody.html", {})


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
