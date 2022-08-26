"""
Модуль со ссылками, связанными с задачами
"""
from django.urls import path

from main import views


urlpatterns = [
    path('list', views.TaskListPage.as_view(), name='task_list'),
    path('create', views.CreateTaskPage.as_view(), name='create_task'),
]
