"""
Модуль с формами
"""
from django import forms
from django.contrib.auth import get_user_model
from django.forms import ClearableFileInput, TextInput, EmailInput

from main.models import UserSettings, Task, Complaint


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


class CreateTaskForm(forms.ModelForm):
    """
    Форма создания задачи
    """

    class Meta:
        model = Task
        fields = ('author', 'title', 'description', 'image', 'answer', 'points', 'score_tier')
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'image': 'Картинка со спрятанным текстом',
            'answer': 'Ответ',
            'points': 'Очки за успешное прохождение задачи',
        }
        widgets = {
            'author': forms.HiddenInput(),
            'image': ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'autocomplete': 'off'}),
            'answer': forms.TextInput(attrs={'autocomplete': 'off'}),
            'score_tier': forms.HiddenInput()
        }


class CreateComplaintForm(forms.ModelForm):
    """
    Форма создания жалобы
    """

    class Meta:
        model = Complaint
        fields = ('author', 'task', 'description')
        labels = {
            'description': 'Причина'
        }
        widgets = {
            'author': forms.HiddenInput(),
            'task': forms.HiddenInput(),
        }
