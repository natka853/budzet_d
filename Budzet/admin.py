from django.contrib import admin

# Register your models here.
from .models import Dochod, Zrodlo, Wydatek, Kategoria

admin.site.register(Dochod)
admin.site.register(Zrodlo)
admin.site.register(Wydatek)
admin.site.register(Kategoria)