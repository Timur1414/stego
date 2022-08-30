"""
Модуль со ссылками, связанными с жалобами
"""
from django.urls import path

from main import views


urlpatterns = [
    path('list/', views.ComplaintListPage.as_view(), name='complaint_list'),
    path('create/<int:task_id>/', views.CreateComplaintPage.as_view(), name='create_complaint'),
    path('<int:pk>/', views.ComplaintPage.as_view(), name='complaint'),
]
