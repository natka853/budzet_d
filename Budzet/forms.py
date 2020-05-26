from django import forms

from .models import Zrodlo
from .models import Kategoria
from .models import Dochod
from .models import Wydatek

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password1',
                  'password2'
                  )


class EditCategoryForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Kategoria
        fields = ('nazwa', )


class EditSourceForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Zrodlo
        fields = ('nazwa', )


class EditIncomeForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Dochod
        fields = (
            'nazwa',
            'zrodlo',
            'opis',
            'data'
        )


class EditExpenseForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Wydatek
        fields = (
            'nazwa',
            'kategoria',
            'opis',
            'data'
        )
