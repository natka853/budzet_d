from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .forms import AdminRegisterForm
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


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = AdminRegisterForm
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_superuser')


admin.site.register(Dochod, DochodAdmin)
admin.site.register(Zrodlo, ZrodloAdmin)
admin.site.register(Wydatek, WydatekAdmin)
admin.site.register(Kategoria, KategoriaAdmin)
admin.site.unregister(Group)

# Changing admin header
admin.site.site_header = "Administracja budżetu domowego"
admin.site.index_title = "Administracja budżetu"
