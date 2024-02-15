from rest_framework import serializers

from main.models import Task, Employee
from main.validators import DateValidator


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        validators = [DateValidator(field='date_constraints')]


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'

