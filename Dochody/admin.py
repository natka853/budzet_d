from django.contrib import admin

# Register your models here.
from .models import Dochod, Zrodlo

admin.site.register(Dochod)
admin.site.register(Zrodlo)