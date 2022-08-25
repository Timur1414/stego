"""
View проекта
"""
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView

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
        usersettings = UserSettings.objects.get(user=user)
        context['user'] = user
        context['username'] = user.username
        context['pagename'] = user.username
        context['avatar'] = usersettings.avatar
        return context
