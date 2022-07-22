"""
View проекта
"""
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse


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


def profile_page():
    pass
