from django.contrib import admin
from .models import Person, Category, Priority, Task


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_by', 'created_at', 'updated_at', 'deleted_at', 'deleted']


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at', 'updated_at', 'deleted_at', 'deleted']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'description', 'completed', 'completed_at', 'created_at', 'updated_at', 'deleted_at', 'deleted']
