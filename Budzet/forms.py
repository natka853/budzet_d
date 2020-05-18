from django import forms

from .models import Zrodlo
from .models import Kategoria
from .models import Dochod
from .models import Wydatek


class ZrodloForm(forms.ModelForm):
    class Meta:
        model = Zrodlo
        fields = (
            'nazwa',
        )


class KategoriaForm(forms.ModelForm):
    class Meta:
        model = Kategoria
        fields = (
            'nazwa',
        )


class DochodForm(forms.ModelForm):
    class Meta:
        model = Dochod
        fields = (
            'nazwa',
            'zrodlo',
            'opis',
            'kwota',
            'data'
        )


class WydatekForm(forms.ModelForm):
    class Meta:
        model = Wydatek
        fields = (
            'nazwa',
            'kategoria',
            'opis',
            'kwota',
            'data'
        )
