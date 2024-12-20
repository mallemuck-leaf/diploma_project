from django.db import models
from django.conf import settings


class Profile(models.Model):
    '''
    The model for account's methods
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Учетная запись {self.user.username}'



