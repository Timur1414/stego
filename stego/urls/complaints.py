"""
Модуль со ссылками, связанными с жалобами
"""
from django.urls import path

from main import views


urlpatterns = [
    path('list/', views.ComplaintListPage.as_view(), name='complaint_list'),
    # path('create/', views., name='create_complaint'),
    # path('<int:pk>/', views., name='complaint'),
]
