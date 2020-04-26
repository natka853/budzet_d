from django.http import HttpResponse
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
