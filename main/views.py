"""
View проекта
"""
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, ListView

from main.forms import UserSettingsEditForm
from main.models import UserSettings


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


def index_page(request):
    context = {
        'pagename': 'Главная'
    }
    return render(request, 'pages/index/index.html', context)


class ProfilePage(LoginRequiredMixin, DetailView):
    """
    Страница профиля
    """
    model = get_user_model()
    template_name = 'pages/profile/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        usersettings = UserSettings.get_usersettings_by_user(user)
        context['user'] = user
        context['username'] = user.username
        context['pagename'] = user.username
        context['avatar'] = usersettings.avatar
        return context


class ProfileSettingsPage(LoginRequiredMixin, UpdateView):
    """
    Страница настроек
    """
    model = get_user_model()
    fields = ['first_name', 'last_name', 'email']
    template_name = 'pages/profile/settings/index.html'

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


class TasksPage(LoginRequiredMixin, ListView):
    """
    Страница со списком задач
    """
    template_name = 'pages/tasks/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        return context
