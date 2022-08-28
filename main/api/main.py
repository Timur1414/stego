"""
Модуль с api функциями
"""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from main.models import Task


@login_required()
def check_answer(request):
    """
    Проверка ответа на задачу
    """
    user_answer = request.GET.get('answer', '')
    id = request.GET.get('id', -1)
    task = Task.get_by_id(id)
    right_answer = task.answer
    if right_answer == user_answer:
        task.set_done(request.user)
    return JsonResponse({
        'is_ok': True if right_answer == user_answer else False,
        'message': '<p class="text-success fs-4">Правильный ответ</p>'
        if right_answer == user_answer else
        '<p class="text-danger fs-4">Неправильный ответ</p>'
    })
