"""
View проекта
"""
from typing import List

from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, ListView, CreateView, TemplateView

from main.forms import UserSettingsEditForm, CreateTaskForm, CreateComplaintForm
from main.models import UserSettings, Task, Complaint
from stego.settings import BASE_URL


@login_required()
def password_change_done(request):
    """
    Кастомная страница с изменением пароля. Сразу переходит на страницу авторизации

    :return: перенаправление на страницу авторизации
    """
    logout(request)
    return redirect('login')


class CustomLoginView(LoginView):
    """
    Кастомный класс авторизации. Изменено перенаправление после авторизации
    """

    def get_success_url(self) -> str:
        """
        Изменение базовой ссылки на ссылку профиля пользователя

        :return: ссылка на профиль пользователя
        :rtype: :class:`str`
        """
        return reverse('profile', kwargs={'pk': self.request.user.id})


class IndexPage(TemplateView):
    """
    Лендинг
    """
    template_name = 'pages/index/index.html'
    extra_context = {
        'BASE_URL': BASE_URL,
        'pagename': 'Главная'
    }


class ProfilePage(LoginRequiredMixin, DetailView):
    """
    Страница профиля
    """
    model = get_user_model()
    template_name = 'pages/profile/index.html'
    extra_context = {
        'BASE_URL': BASE_URL
    }

    def get_context_data(self, **kwargs) -> dict:
        """
        Формирование словаря для наполнения страницы
        """
        context = super().get_context_data(**kwargs)
        usersettings = UserSettings.get_usersettings_by_user(self.object)
        context['user'] = self.object
        context['pagename'] = self.object.username
        context['avatar'] = usersettings.avatar
        if self.object == self.request.user:
            tasks_to_history = Task.get_done_tasks(self.object)
            context['count_of_tasks_to_history'] = len(tasks_to_history)
            tasks_to_history = tasks_to_history[:5]
            context['tasks_to_history'] = [
                [task, task.get_done_count()] for task in tasks_to_history
            ]
        created_tasks = Task.get_tasks_of_user(self.object)
        context['count_of_created_tasks'] = len(created_tasks)
        created_tasks = created_tasks[:5]
        context['created_tasks'] = [
            [task, task.get_done_count()] for task in created_tasks
        ]
        context['suggestion_task'] = Task.get_suggestion_task(self.object)
        return context


class ProfileSettingsPage(LoginRequiredMixin, UpdateView):
    """
    Страница настроек
    """
    model = get_user_model()
    fields = ['first_name', 'last_name', 'email']
    template_name = 'pages/profile/settings/index.html'
    extra_context = {
        'BASE_URL': BASE_URL,
        'pagename': 'Настройки'
    }

    def get_success_url(self) -> str:
        """
        Определение URL, на которую нужно перейти в случае, если данные будут записаны успешно

        :return: строка с готовым URL
        :rtype: :class:`str`
        """
        return reverse("profile", kwargs={'pk': self.object.id})

    def get_object(self, queryset=None) -> get_user_model:
        """
        Получение user'а
        Берётся активный в данный момент пользователь, чтобы не просматривать чужие настройки
        """
        return self.request.user

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """
        Обработчик POST-запроса на данной странице.

        Кроме базового сохранения формы - проверяем и сохраняет UserSettings'ы.

        :param request: словарь с параметрами POST-запроса
        :return: объект HttpResponse с редиректом внутри.
        :rtype: :class:`django.http.HttpResponse`
        """
        usersettings_form = UserSettingsEditForm(
            instance=self.request.user.usersettings,
            data=self.request.POST,
            files=self.request.FILES
        )
        if usersettings_form.is_valid():
            usersettings_form.save()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        """
        Формирование словаря для наполнения страницы
        """
        context = super().get_context_data(**kwargs)
        context['settings_form'] = UserSettingsEditForm(instance=self.request.user.usersettings)
        return context


class HistoryPage(LoginRequiredMixin, ListView):
    """
    Страница с историей выполненных задач
    """
    template_name = 'pages/profile/history/index.html'
    model = get_user_model()
    context_object_name = 'context'
    extra_context = {
        'BASE_URL': BASE_URL,
        'pagename': 'История'
    }

    def get_queryset(self) -> List:
        """
        Получение списка выполненных задач
        """
        tasks_to_history = Task.get_done_tasks(self.request.user)
        return [
            [task, task.get_done_count()] for task in tasks_to_history
        ]


class CreatedTasksPage(LoginRequiredMixin, DetailView):
    """
    Страница со списком задач, созданных пользователем
    """
    model = get_user_model()
    template_name = 'pages/profile/created_tasks/index.html'
    extra_context = {
        'BASE_URL': BASE_URL,
        'pagename': 'Созданные задачи'
    }

    def get_context_data(self, **kwargs) -> dict:
        """
        Формирование словаря для наполнения страницы
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.object
        created_tasks = Task.get_tasks_of_user(self.object)
        context['created_tasks'] = [
            [task, task.get_done_count()] for task in created_tasks
        ]
        return context


class EducationPage(LoginRequiredMixin, TemplateView):
    """
    Страница с обучением
    """
    template_name = 'pages/profile/education/index.html'
    extra_context = {
        'BASE_URL': BASE_URL,
        'pagename': 'Обучение'
    }


class TaskListPage(LoginRequiredMixin, ListView):
    """
    Страница со списком задач
    """
    template_name = 'pages/tasks/list.html'
    model = Task
    context_object_name = 'context'
    extra_context = {
        'BASE_URL': BASE_URL,
        'pagename': 'Список задач'
    }

    def get_queryset(self) -> List:
        """
        Получение активных задач
        """
        tasks = Task.get_active()
        return [
            [task, task.is_done(self.request.user)] for task in tasks
        ]


class TaskPage(LoginRequiredMixin, DetailView):
    """
    Страница задачи
    """
    model = Task
    template_name = 'pages/tasks/index.html'
    extra_context = {
        'BASE_URL': BASE_URL
    }

    def get_context_data(self, **kwargs) -> dict:
        """
        Формирование словаря для наполнения страницы
        """
        context = super().get_context_data(**kwargs)
        if not self.object.active:
            raise Http404
        context['pagename'] = self.object.title
        context['task'] = self.object
        context['done'] = self.object.is_done(self.request.user)
        context['done_count'] = self.object.get_done_count()
        return context


class CreateTaskPage(LoginRequiredMixin, CreateView):
    """
    Страница создания задачи
    """
    model = Task
    fields = ['author', 'title', 'description', 'image', 'answer', 'points', 'score_tier']
    template_name = 'pages/tasks/create.html'
    extra_context = {
        'BASE_URL': BASE_URL,
        'pagename': 'Создание задачи'
    }

    def get_success_url(self) -> str:
        """
        Получение перенаправляющей ссылки при успешном создании задачи
        """
        return reverse('task', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs) -> dict:
        """
        Формирование словаря для наполнения страницы
        """
        context = super().get_context_data(**kwargs)
        context['form'] = CreateTaskForm(initial={
            'author': self.request.user,
            'score_tier': self.request.user.usersettings.score
        })
        return context


class ComplaintListPage(LoginRequiredMixin, ListView):
    """
    Страница со списком жалоб
    Доступна только администраторам
    """
    template_name = 'pages/tasks/complaints/list.html'
    context_object_name = 'context'
    extra_context = {
        'BASE_URL': BASE_URL,
        'pagename': 'Список жалоб'
    }

    def get_queryset(self) -> List:
        """
        Получение жалоб и проверка на администратора
        """
        if not self.request.user.is_staff:
            raise Http404
        return Complaint.get_active()


class CreateComplaintPage(LoginRequiredMixin, CreateView):
    """
    Страница создания жалобы
    """
    model = Complaint
    fields = ['author', 'task', 'description']
    template_name = 'pages/tasks/complaints/create.html'
    extra_context = {
        'BASE_URL': BASE_URL,
        'pagename': 'Создание жалобы'
    }

    def get_success_url(self) -> str:
        """
        Получение перенаправляющей ссылки при успешном создании жалобы
        """
        return reverse('task_list')

    def get_context_data(self, **kwargs) -> dict:
        """
        Формирование словаря для наполнения страницы
        """
        context = super().get_context_data(**kwargs)
        task = Task.get_by_id(self.kwargs['task_id'])
        context['task'] = task
        context['form'] = CreateComplaintForm(initial={
            'author': self.request.user,
            'task': task
        })
        return context


class ComplaintPage(LoginRequiredMixin, DetailView):
    """
    Страница просмотра жалобы
    Доступна только администраторам
    """
    model = Complaint
    template_name = 'pages/tasks/complaints/index.html'
    extra_context = {
        'BASE_URL': BASE_URL,
        'pagename': 'Жалоба'
    }

    def post(self, request, *args, **kwargs) -> redirect:
        """
        Обработчик POST-запроса
        """
        action = request.POST.get('action')
        complaint = Complaint.get_by_id(self.kwargs['pk'])
        if action == 'accept':
            complaint.accept()
        elif action == 'dismiss':
            complaint.dismiss()
        return redirect(to='complaint_list')

    def get_context_data(self, **kwargs) -> dict:
        """
        Формирование словаря для наполнения страницы
        """
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_staff:
            raise Http404
        context['complaint'] = self.object
        return context
