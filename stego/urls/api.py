"""
Модуль со ссылками, связанными с api
"""
from django.urls import path

from main.api import main


urlpatterns = [
    path('check_answer/', main.check_answer),
    path('tasks_search/', main.tasks_search),
]
