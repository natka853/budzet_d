from django.contrib import admin

# Register your models here.
from .models import Wydatek, Kategoria

admin.site.register(Wydatek)
admin.site.register(Kategoria)