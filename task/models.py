from django.db import models
from django.conf import settings


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        if self.user.first_name is not None and self.user.last_name is not None:
            return f'{self.user.first_name} {self.user.last_name}'
        if self.user.first_name is not None:
            return f'{self.user.first_name} -'
        if self.user.last_name is not None:
            return f'- {self.user.last_name}'
        return f'{self.user.username}'
