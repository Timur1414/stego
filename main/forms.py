"""
Модуль с формами
"""
from django import forms
from django.contrib.auth import get_user_model
from django.forms import ClearableFileInput, TextInput, EmailInput

from main.models import UserSettings


class UserEditForm(forms.ModelForm):
    """
    Форма редактирования основных данных пользователя
    """

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
        }


class UserSettingsEditForm(forms.ModelForm):
    """
    Форма редактирования настроек пользователя
    """

    class Meta:
        model = UserSettings
        fields = ('avatar',)
        labels = {'avatar': 'Аватар'}
        widgets = {
            'avatar': ClearableFileInput(attrs={'class': 'form-control'})
        }

