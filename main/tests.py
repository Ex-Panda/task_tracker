from unittest import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Employee, Task


class EmployeeTestCase(APITestCase):
    """Тестирование создания сотрудника"""

    def setUp(self) -> None:
        pass

    def test_employee_creation(self):

        data = {
            'name': 'Иванов Иван Иваныч',
            'position': 'Разработчик'
        }
        response = self.client.post(
            '/employees/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id':response.json()['id'], 'name': 'Иванов Иван Иваныч', 'position': 'Разработчик'}
        )

        self.assertTrue(
            Employee.objects.all().exists()
        )

    def test_employee_list(self):

        employee = Employee.objects.create(
            name='Иванов Иван Иваныч',
            position='Разработчик'
        )

        response = self.client.get(
            '/employees/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{'id': employee.id, 'name': 'Иванов Иван Иваныч', 'position': 'Разработчик'}]
        )

    def test_employee_detail(self):

        employee = Employee.objects.create(
            name='Иванов Иван Иваныч',
            position='Разработчик'
        )

        response = self.client.get(
            f'/employees/{employee.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': employee.id, 'name': 'Иванов Иван Иваныч', 'position': 'Разработчик'}
        )

    def test_employee_update(self):

        employee = Employee.objects.create(
            name='Иванов Иван Иваныч',
            position='Разработчик'
        )

        data = {
            'name': 'Андреев Андрей Андреевич'
        }

        response = self.client.patch(
            f'/employees/{employee.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['name'],
            'Андреев Андрей Андреевич'
        )

    def test_employee_delete(self):

        employee = Employee.objects.create(
            name='Иванов Иван Иваныч',
            position='Разработчик'
        )

        response = self.client.delete(
            f'/employees/{employee.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class TaskTestCase(APITestCase):

    def setUp(self):

        pass

    def test_task_create(self):

        data = {
            'title': 'Тестовая задача',
            'reference': '',
            'employee': '',
            'date_constraints': '2024-03-20',
            'status': 'active'
        }
        response = self.client.post(
            '/tasks/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Task.objects.all().exists()
        )

    def test_task_list(self):

        task = Task.objects.create(
            title='Тестовая задача',
            reference=None,
            employee=None,
            date_constraints='2024-03-20',
            status='active'
        )
        response = self.client.get(
            '/tasks/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{'id': task.id, 'title': 'Тестовая задача', 'reference': None,
              'employee': None, 'date_constraints': '2024-03-20', 'status': 'active'}]
        )

    def test_task_detail(self):
        task = Task.objects.create(
            title='Тестовая задача',
            reference=None,
            employee=None,
            date_constraints='2024-03-20',
            status='active'
        )
        response = self.client.get(
            f'/tasks/{task.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': task.id, 'title': 'Тестовая задача', 'reference': None, 'employee': None,
             'date_constraints': '2024-03-20', 'status': 'active'}
        )

    def test_task_update(self):

        task = Task.objects.create(
            title='Тестовая задача',
            reference=None,
            employee=None,
            date_constraints='2024-03-20',
            status='active'
        )
        data = {
            'title': 'Приоритетная тестовая задача'
        }

        response = self.client.patch(
            f'/tasks/{task.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['title'],
            'Приоритетная тестовая задача'
        )

    def test_task_delete(self):

        task = Task.objects.create(
            title='Тестовая задача',
            reference=None,
            employee=None,
            date_constraints='2024-03-20',
            status='active'
        )

        response = self.client.delete(
            f'/tasks/{task.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class ImportantTaskTestCase(APITestCase):

    def setUp(self):
        employee_1 = Employee.objects.create(
            name='Иванов Иван Иваныч',
            position='Разработчик'
        )
        employee_2 = Employee.objects.create(
            name='Андреев Андрей Андреевич',
            position='Разработчик'
        )

        task_1 = Task.objects.create(
            title='Важная задача',
            reference=None,
            employee=employee_2,
            date_constraints='2024-03-20',
            status='active'
        )

        task_2 = Task.objects.create(
            title='Новая задача',
            reference=task_1,
            employee=None,
            date_constraints='2024-02-28',
            status='active'
        )

    def test_get_employees(self):

        response = self.client.get(
            '/important_task/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{'title': 'Новая задача', 'date_constraints': '2024-02-28',
              'employee': ['Андреев Андрей Андреевич', 'Иванов Иван Иваныч']}]
        )


class BusyEmployeesTestCase(APITestCase):

    def setUp(self):

        employee_1 = Employee.objects.create(
            name='Иванов Иван Иваныч',
            position='Разработчик'
        )
        employee_2 = Employee.objects.create(
            name='Андреев Андрей Андреевич',
            position='Разработчик'
        )

        employee_3 = Employee.objects.create(
            name='Андреев Роман Романыч',
            position='Разработчик'
        )

        task_1 = Task.objects.create(
            title='Важная задача',
            reference=None,
            employee=employee_1,
            date_constraints='2024-03-20',
            status='active'
        )

        task_2 = Task.objects.create(
            title='Новая задача',
            reference=task_1,
            employee=employee_3,
            date_constraints='2024-02-28',
            status='active'
        )
        task_3 = Task.objects.create(
            title='Самая новая задача',
            reference=None,
            employee=employee_1,
            date_constraints='2024-02-28',
            status='active'
        )

    def test_get_employees(self):

        response = self.client.get(
            '/busy_employee/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{'name': 'Андреев Андрей Андреевич', 'task': []},
             {'name': 'Андреев Роман Романыч', 'task': ['Новая задача']},
             {'name': 'Иванов Иван Иваныч', 'task': ['Важная задача', 'Самая новая задача']}]
        )





