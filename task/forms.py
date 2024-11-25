from django import forms
from .models import Task, Category, Priority, Status


class TaskCreateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'category', 'priority']


class TaskUpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status',]


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'status', 'category', 'priority']


class TaskDeleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = []


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class CategoryDeleteForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = []


class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ['name',]


class PriorityDeleteForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = []


class TaskStatusFilterForm(forms.Form):
    status = forms.ChoiceField(choices=Status.choices,
                               label='Фильтр задач по статусу:')


SortingChoices = (
        ('status', 'статус'),
        ('created_at', 'дата создания'),
        # ('completed', 'срок выполнения'),
    )


class TaskSortingForm(forms.Form):
    filter_choice = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                              choices=SortingChoices,
                                              label='Сортировка задач:')
