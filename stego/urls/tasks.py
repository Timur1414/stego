"""
Модуль со ссылками, связанными с задачами
"""
from django.urls import path

from main import views


urlpatterns = [
    path('list', views.TasksPage.as_view(), name='task_list'),

]