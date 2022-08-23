"""
Модуль с моделями
"""
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserSettings(models.Model):
    """
    Модель настроек пользователя
    """
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/users/', default='images/users/no_avatar.png')


@receiver(post_save, sender=get_user_model())
def update_profile_signal(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    """
    Обработчик создания юзера

    :param sender: источник сигнала
    :param instance: созданный объект
    :param created: признак того, что объект был создан (или изменён)
    :param kwargs: всё остальное
    """
    if not created:
        return
    UserSettings.objects.create(user=instance)
