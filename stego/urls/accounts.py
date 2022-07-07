"""
Модуль со ссылками, связанными с аккаунтами
"""
from django.urls import path, include
from django.contrib.auth.views import PasswordChangeView
from django_registration.backends.one_step.views import RegistrationView

from main import views

urlpatterns = [
    path(
        'login/',
        views.CustomLoginView.as_view(
            extra_context={
                'pagename': 'Авторизация'
            },
        ),
        name='login'
    ),
    path('register/', RegistrationView.as_view(
        extra_context={
            'pagename': 'Регистрация'
        },
    ), name='django_registration_register'),
    path(
        'password_change/',
        PasswordChangeView.as_view(
            extra_context={
                'pagename': 'Смена пароля'
            },
        ), name='password_change'),
    path('password_change/done/', views.password_change_done, name='password_change_done'),
    path('', include('django_registration.backends.one_step.urls')),
    path('', include('django.contrib.auth.urls')),
    # path('profile/<int:pk>/', views.ProfilePage.as_view(), name='profile'),
    # path('profile/<int:pk>/settings/', views.ProfileSettings.as_view(), name='profile_settings'),
]
