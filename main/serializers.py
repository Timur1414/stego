from rest_framework import serializers

from main.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для задач на странице списка задач
    """
    class Meta:
        model = Task
        fields = ['id', 'title']
