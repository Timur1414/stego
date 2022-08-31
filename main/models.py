"""
Модуль с моделями
"""
from typing import List

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
    score = models.IntegerField(default=0)

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

    def add_score(self, score: int):
        """
        Добавление очков
        """
        self.score += score


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

    :param author: автор задачи
    :param title: заголовок задачи
    :param description: описание задачи
    :param image: изображение со спрятанным текстом
    :param answer: ответ
    :param points: очки, которые получит пользователь при решении задачи
    :param group: группа (блок) задачи
    :param created: дата создания задачи
    :param active: параметр, отвечающий за блокировку
    :param done: параметр, отвечающий за выполнение
    """
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/tasks/')
    answer = models.CharField(max_length=255)
    points = models.IntegerField()
    group = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(default=True)
    done = models.ManyToManyField(to=get_user_model())

    @staticmethod
    def get_tasks_of_user(user: get_user_model()) -> List:
        """
        Получение задач, которые создал пользователь
        """
        return Task.objects.filter(author=user, active=True)

    def get_done_count(self) -> int:
        """
        Получение количества пользователей, решивших задачу
        """
        return self.done.count()

    @staticmethod
    def get_done_tasks(user: get_user_model()) -> List:
        """
        Получение сделаных задач
        """
        tasks = Task.get_active()
        result = []
        for task in tasks:
            if user in task.done.all():
                result.append(task)
        return result

    def is_done(self, user: get_user_model()) -> bool:
        """
        Проверка на то, сделана ли задача
        """
        return user in self.done.all()

    def set_done(self, user: get_user_model()):
        """
        Обновление задачи при решении
        """
        self.done.add(user)

    @staticmethod
    def get_by_id(id: int):
        """
        Получение задачи по id
        """
        try:
            return Task.objects.get(id=id)
        except Task.DoesNotExist:
            return None

    @staticmethod
    def get_active() -> List:
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

    @staticmethod
    def get_by_title(title: str):
        """
        Получение задач по названию
        """
        return Task.objects.filter(active=True, title=title)


class Complaint(models.Model):
    """
    Модель жалобы
    Состояния:
        0 - на рассмотрении
        1 - принято
        2 - отказано
    """
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    state = models.IntegerField(default=0)

    @staticmethod
    def get_by_id(id: int):
        """
        Получение жалобы по id
        """
        try:
            return Complaint.objects.get(id=id)
        except Complaint.DoesNotExist:
            return None

    def accept(self):
        """
        Принятие жалобы и блокировка задачи
        """
        self.state = 1
        self.task.active = False
        self.save()
        self.task.save()
        complaints = Complaint.get_complaints_of_task(self.task)
        for complaint in complaints:
            complaint.dismiss()

    def dismiss(self):
        """
        Отклонение жалобы
        """
        self.state = 2
        self.save()

    @staticmethod
    def get_complaints_of_task(task: Task, state: int = 0) -> List:
        """
        Получение всех жалоб на задачу
        """
        return Complaint.objects.filter(task=task, state=state)

    @staticmethod
    def get_active() -> List:
        """
        Получение жалоб "на рассмотрении"
        """
        return Complaint.objects.filter(state=0)
