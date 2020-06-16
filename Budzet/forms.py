from .models import Zrodlo
from .models import Kategoria
from .models import Dochod
from .models import Wydatek

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SourceForm(forms.ModelForm):
    class Meta:
        model = Zrodlo
        fields = (
            'nazwa',
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Kategoria
        fields = (
            'nazwa',
        )


class IncomeForm(forms.ModelForm):
    data = forms.DateField(required=False)

    class Meta:
        model = Dochod
        fields = (
            'nazwa',
            'zrodlo',
            'opis',
            'kwota',
            'data'
        )


class ExpenseForm(forms.ModelForm):
    data = forms.DateField(required=False)

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


class AdminRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password1',
                  'password2',
                  )


class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Kategoria
        fields = ('nazwa',)


class EditSourceForm(forms.ModelForm):
    class Meta:
        model = Zrodlo
        fields = ('nazwa',)


class EditIncomeForm(forms.ModelForm):
    nazwa = forms.CharField(required=False)
    kwota = forms.DecimalField(required=False)
    data = forms.CharField(required=False)

    class Meta:
        model = Dochod
        fields = (
            'nazwa',
            'zrodlo',
            'opis',
            'kwota',
            'data'
        )


class EditExpenseForm(forms.ModelForm):
    nazwa = forms.CharField(required=False)
    kwota = forms.DecimalField(required=False)
    data = forms.CharField(required=False)

    class Meta:
        model = Wydatek
        fields = (
            'nazwa',
            'kategoria',
            'opis',
            'kwota',
            'data'
        )
