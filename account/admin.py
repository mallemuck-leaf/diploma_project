from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''
    Registration model Profile in admin panel.
    '''
    list_display = ['user', 'date_of_birth']
    raw_id_fields = ['user',]
