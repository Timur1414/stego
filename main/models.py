"""
Модуль с моделями
"""
from django.contrib.auth import get_user_model
from django.db import models


class UserSettings(models.Model):
    """
    Модель настроек пользователя
    """
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/users/', default='images/users/no_avatar.png')
