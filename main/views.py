from django.db.models import Count, Min
from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Employee, Task
from main.serializers import EmployeeSerializer, TaskSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ImportantTaskAPIView(APIView):

    def get(self, request):

        tasks = Task.objects.all()
        list_dict_task = []
        min_count_task = Employee.objects.annotate(task_count=Count('task')).aggregate(min_task_count=Min('task_count'))['min_task_count']
        for task in tasks:
            if task.reference is not None and task.employee is None and task.reference.employee is not None:
                dict_task = {
                    "title": task.title,
                    "date_constraints": task.date_constraints,
                    "employee": []
                }
                if task.reference.employee.task_set.count() <= min_count_task + 2:
                    dict_task["employee"].append(task.reference.employee.name)

                list_employees_min_task = Employee.objects.annotate(task_count=Count('task')).filter(task_count=min_count_task)

                for employee in list_employees_min_task:
                    if employee.name not in dict_task["employee"]:
                        dict_task["employee"].append(employee.name)

                list_dict_task.append(dict_task)

        return Response(list_dict_task)


class BusyEmployeesAPIView(APIView):

    def get(self, request):

        employees = Employee.objects.all()
        list_employees = []

        for employee in employees:
            list_task = []
            employee_name = employee.name
            tasks = employee.task_set.filter(status='active')
            for task in tasks:
                list_task.append(task.title)
            dict_employee = {'name': employee_name, 'task': list_task}
            list_employees.append(dict_employee)

        sorted_list_employees = sorted(list_employees, key=lambda x: len(x['task']))

        return Response(sorted_list_employees)
