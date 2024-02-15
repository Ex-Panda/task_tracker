from django.utils import timezone
from rest_framework.serializers import ValidationError


class DateValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        date_constraints = dict(value).get(self.field)
        now = timezone.now()

        if date_constraints is not None and date_constraints < now.date():
            raise ValidationError('Дата выполнения задачи не может быть раньше текущего дня')

