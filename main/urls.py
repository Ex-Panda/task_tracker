from django.urls import path
from rest_framework.routers import DefaultRouter

from main.apps import MainConfig
from main.views import TaskViewSet, EmployeeViewSet, ImportantTaskAPIView, BusyEmployeesAPIView

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'employees', EmployeeViewSet, basename='employees')

urlpatterns = [
    path('important_task/', ImportantTaskAPIView.as_view(), name='important_task'),
    path('busy_employee/', BusyEmployeesAPIView.as_view(), name='busy_employee')
] + router.urls
