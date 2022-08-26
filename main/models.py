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

    @staticmethod
    def get_usersettings_by_user(user: get_user_model):
        """
        Получение usersettings о user
        """
        usersettings, created = UserSettings.objects.get_or_create(
            user=user
        )
        if created:
            usersettings.save()
        return usersettings


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


class Task(models.Model):
    """
    Модель задачи
    """
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/tasks/')
    answer = models.CharField(max_length=255)
    points = models.IntegerField()
    group = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(default=True)

    @staticmethod
    def get_active():
        """
        Получение только активных задач
        """
        return Task.objects.filter(active=True)

    @staticmethod
    def get_by_group(group: str):
        """
        Получение задач по группе (блоку)
        """
        return Task.objects.filter(active=True, group=group)
