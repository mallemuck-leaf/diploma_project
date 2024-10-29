from django.contrib import admin
from .models import Person, Category, Priority, Task


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user']


