from django.db import models
from django.db.models import SET_NULL

NULLABLE = {'blank': True, 'null': True}


class Employee(models.Model):
    name = models.CharField(max_length=255, verbose_name="ФИО")
    position = models.CharField(max_length=255, verbose_name="должность")


class Task(models.Model):

    STATUS = (
        ('active', 'активная'),
        ('completed', 'завершенная')
    )

    title = models.CharField(max_length=255, verbose_name='название')
    reference = models.ForeignKey('Task', on_delete=SET_NULL, verbose_name='ссылка на родительскую задачу', **NULLABLE)
    employee = models.ForeignKey('Employee', on_delete=SET_NULL, verbose_name='исполнитель', **NULLABLE)
    date_constraints = models.DateField(verbose_name='дата исполенения')
    status = models.CharField(choices=STATUS, verbose_name='статус')
