from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_widok(request, *args, **kwargs):
  #  return HttpResponse("<h1>Budżet domowy</h1>")
    return render(request, "home.html", {})

def dochody(*args, **kwargs):
    return HttpResponse("<h1>Tu są twoje dochody</h1>")

def wydatki(*args, **kwargs):
    return HttpResponse("<h1>Tu są twoje wydatki</h1>")
