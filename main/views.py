"""
View проекта
"""
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, ListView, CreateView, TemplateView

from main.forms import UserSettingsEditForm, CreateTaskForm
from main.models import UserSettings, Task
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        usersettings = UserSettings.get_usersettings_by_user(user)
        context['user'] = user
        context['username'] = user.username
        context['pagename'] = user.username
        context['avatar'] = usersettings.avatar
        if user == self.request.user:
            tasks_to_history = Task.get_done_tasks(self.object)
            context['count_of_tasks_to_history'] = len(tasks_to_history)
            tasks_to_history = tasks_to_history[:5]
            context['tasks_to_history'] = [
                [task, task.get_done_count()] for task in tasks_to_history
            ]
        created_tasks = Task.get_tasks_of_user(user)
        context['count_of_created_tasks'] = len(created_tasks)
        created_tasks = created_tasks[:5]
        context['created_tasks'] = [
            [task, task.get_done_count()] for task in created_tasks
        ]
        return context


class ProfileSettingsPage(LoginRequiredMixin, UpdateView):
    """
    Страница настроек
    """
    model = get_user_model()
    fields = ['first_name', 'last_name', 'email']
    template_name = 'pages/profile/settings/index.html'
    extra_context = {
        'BASE_URL': BASE_URL
    }

    def get_success_url(self) -> str:
        """
        Определение URL, на которую нужно перейти в случае, если данные будут записаны успешно

        :return: строка с готовым URL
        :rtype: :class:`str`
        """
        return reverse("profile", kwargs={'pk': self.object.id})

    def get_object(self, queryset=None):
        """
        Получение user'а
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Настройки'
        user = self.object
        usersettings = UserSettings.objects.get(user=user)
        context['settings_form'] = UserSettingsEditForm(instance=self.request.user.usersettings)
        return context


class HistoryPage(LoginRequiredMixin, DetailView):
    """
    Страница с историей выполненных задач
    """
    template_name = 'pages/profile/history/index.html'
    model = get_user_model()
    extra_context = {
        'BASE_URL': BASE_URL
    }

    def get_object(self, queryset=None):
        """
        Получение user'а
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'История'
        tasks_to_history = Task.get_done_tasks(self.object)
        context['tasks_to_history'] = [
            [task, task.get_done_count()] for task in tasks_to_history
        ]
        return context


class CreatedTasksPage(LoginRequiredMixin, DetailView):
    """
    Страница со списком задач, созданных пользователем
    """
    model = get_user_model()
    template_name = 'pages/profile/created_tasks/index.html'
    extra_context = {
        'BASE_URL': BASE_URL
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Созданные задачи'
        context['user'] = self.object
        created_tasks = Task.get_tasks_of_user(self.object)
        context['created_tasks'] = [
            [task, task.get_done_count()] for task in created_tasks
        ]
        return context


class TaskListPage(LoginRequiredMixin, ListView):
    """
    Страница со списком задач
    """
    template_name = 'pages/tasks/list.html'
    model = Task
    extra_context = {
        'BASE_URL': BASE_URL
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['pagename'] = 'Список задач'
        tasks = Task.get_active()
        context['tasks'] = [
            [task, task.is_done(self.request.user)] for task in tasks
        ]
        return context


class TaskPage(LoginRequiredMixin, DetailView):
    """
    Страница задачи
    """
    model = Task
    template_name = 'pages/tasks/index.html'
    extra_context = {
        'BASE_URL': BASE_URL
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        if not task.active:
            raise Http404
        context['pagename'] = task.title
        context['task'] = task
        context['done'] = task.is_done(self.request.user)
        context['done_count'] = task.get_done_count()
        return context


class CreateTaskPage(LoginRequiredMixin, CreateView):
    """
    Страница создания задачи
    """
    model = Task
    fields = ['author', 'title', 'description', 'image', 'answer', 'points', 'group']
    template_name = 'pages/tasks/create.html'
    extra_context = {
        'BASE_URL': BASE_URL
    }

    def get_success_url(self):
        """
        Получение перенаправляющей ссылки при успешном создании задачи
        """
        return reverse('task', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Создание задачи'
        context['form'] = CreateTaskForm(initial={'author': self.request.user})
        return context
