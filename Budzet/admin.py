from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from .models import Dochod, Zrodlo, Wydatek, Kategoria


class DochodAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'zrodlo', 'opis', 'kwota', 'data')
    list_filter = ('zrodlo', 'data')


class WydatekAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'kategoria', 'opis', 'kwota', 'data')
    list_filter = ('kategoria', 'data')


class KategoriaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'user')
    list_filter = ('user', )


class ZrodloAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'user')
    list_filter = ('user', )


admin.site.register(Dochod, DochodAdmin)
admin.site.register(Zrodlo, ZrodloAdmin)
admin.site.register(Wydatek, WydatekAdmin)
admin.site.register(Kategoria, KategoriaAdmin)
admin.site.unregister(Group)

# Changing admin header
admin.site.site_header = "Administracja budżetu domowego"
admin.site.index_title = "Administracja budżetu"

