from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, Priority, Category, Person
from .forms import (
    TaskCreateForm, TaskUpdateForm, TaskUpdateStatusForm, TaskDeleteForm,
    PriorityForm, PriorityDeleteForm,
    CategoryForm, CategoryDeleteForm,
    TaskStatusFilterForm, TaskSortingForm
)


@login_required
def task_list(request):
    user = Person.objects.get(user=request.user)
    tasks = Task.objects.filter(deleted_at=None, deleted=None)
    filter_form = TaskStatusFilterForm(data=request.GET)
    sorted_form = TaskSortingForm(data=request.GET)
    if filter_form.is_valid():
        if filter_form.cleaned_data['status']:
            tasks = tasks.filter(status=filter_form.cleaned_data['status'])
    if sorted_form.is_valid():
        if sorted_form.cleaned_data['filter_choice']:
            sort_items = sorted_form.cleaned_data['filter_choice']
        # else:
        #     sort_items = ['created_by', ]
    else:
        sort_items = ['created_by',]
    if request.user.is_staff:
        content = {
            'tasks': tasks.order_by(*sort_items),
            'filter_form': filter_form,
            'sorted_form': sorted_form,
        }
    else:
        content = {
            'tasks': tasks.filter(created_by=user).order_by(*sort_items),
            'filter_form': filter_form,
            'sorted_form': sorted_form,
        }
    return render(request, 'task/task_list.html', content)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskCreateForm(data=request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.created_by = Person.objects.get(user=request.user)
            new_task.save()
            return redirect('/tasks/')
        else:
            messages.error(request, 'New task error.')
    form = TaskCreateForm()
    content = {
        'form': form,
    }
    return render(request, 'task/task_create.html', content)


@login_required
def task_detail(request, pk):
    task_obj = Task.objects.get(id=pk)
    if request.method == 'POST':
        form = TaskUpdateStatusForm(data=request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            Task.objects.filter(id=pk).update(status=new_task.status,
                                              updated_at=datetime.now())
            return redirect(f'/tasks/{pk}')
        else:
            messages.error(request, 'New task error.')
    form = TaskUpdateStatusForm(instance=task_obj)
    content = {
        'form': form,
        'task': task_obj,
    }
    return render(request, 'task/task_detail.html', content)


@login_required
def task_update(request, pk):
    task_obj = Task.objects.get(id=pk)
    if request.method == 'POST':
        form = TaskUpdateForm(data=request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            Task.objects.filter(id=pk).update(title=new_task.title,
                                              description=new_task.description,
                                              completed=new_task.completed,
                                              category=new_task.category,
                                              priority=new_task.priority,
                                              status=new_task.status,
                                              updated_at=datetime.now())
            return redirect(f'/tasks/{pk}')
        else:
            messages.error(request, 'New task error.')
    form = TaskUpdateForm(instance=task_obj)
    content = {
        'form': form,
        # 'task': task_obj,
    }
    return render(request, 'task/task_detail.html', content)


@login_required
def task_delete(request, pk):
    if request.method == 'POST':
        form = TaskDeleteForm(data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            if request.user.is_staff:
                Task.objects.filter(id=pk).update(deleted=datetime.now())
            else:
                Task.objects.filter(id=pk).update(deleted_at=datetime.now())
            responce = redirect('/tasks/')
            return responce
    form = TaskDeleteForm()
    content = {
        'task': Task.objects.get(id=pk),
        'form': form,
    }
    return render(request, 'task/task_delete.html', content)


@login_required
def priority_list(request):
    if request.method == 'POST':
        form = PriorityForm(data=request.POST)
        if form.is_valid():
            new_priority = form.save(commit=False)
            new_priority.created_by = Person.objects.get(user=request.user)
            new_priority.save()
            messages.success(request, 'New priority added.')
        else:
            messages.error(request, 'New priority error.')
        return redirect('/tasks/priorities/')
    form = PriorityForm()
    user = Person.objects.get(user=request.user)
    if request.user.is_staff:
        content = {
            'priorities': Priority.objects.filter(deleted_at=None, deleted=None).order_by('created_by'),
            'form': form,
        }
    else:
        content = {
            'priorities': Priority.objects.filter(created_by=user, deleted_at=None, deleted=None),
            'form': form,
        }
    return render(request, 'task/priority_list.html', content)


@login_required
def priority_update(request, pk):
    if request.method == 'POST':
        form = PriorityForm(data=request.POST)
        if form.is_valid():
            updated_priority = form.save(commit=False)
            Priority.objects.filter(id=pk).update(name=updated_priority.name, updated_at=datetime.now())
            return redirect('/tasks/priorities/')
    form = PriorityForm()
    content = {
        'priority': Priority.objects.get(id=pk),
        'form': form,
    }
    return render(request, 'task/priority_update.html', content)


@login_required
def priority_delete(request, pk):
    if request.method == 'POST':
        form = PriorityDeleteForm(data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            if request.user.is_staff:
                Priority.objects.filter(id=pk).update(deleted=datetime.now())
            else:
                Priority.objects.filter(id=pk).update(deleted_at=datetime.now())
            responce = redirect('/tasks/priorities/')
            return responce
    form = PriorityDeleteForm()
    content = {
        'priority': Priority.objects.get(id=pk),
        'form': form,
    }
    return render(request, 'task/priority_delete.html', content)


@login_required
def category_list(request):
    if request.method == 'POST':
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.created_by = Person.objects.get(user=request.user)
            new_category.save()
            messages.success(request, 'New category added.')
        else:
            messages.error(request, 'New category error.')
        return redirect('/tasks/categories/')
    form = CategoryForm()
    user = Person.objects.get(user=request.user)
    if request.user.is_staff:
        content = {
            'categories': Category.objects.filter(deleted_at=None, deleted=None).order_by('created_by'),
            'form': form,
        }
    else:
        content = {
            'categories': Category.objects.filter(created_by=user, deleted_at=None, deleted=None),
            'form': form,
        }
    return render(request, 'task/category_list.html', content)


@login_required
def category_update(request, pk):
    if request.method == 'POST':
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            updated_category = form.save(commit=False)
            Category.objects.filter(id=pk).update(name=updated_category.name,
                                                  description=updated_category.description,
                                                  updated_at=datetime.now())
            return redirect('/tasks/categories/')
    form = CategoryForm()
    content = {
        'category': Category.objects.get(id=pk),
        'form': form,
    }
    return render(request, 'task/category_update.html', content)


@login_required
def category_delete(request, pk):
    if request.method == 'POST':
        form = CategoryDeleteForm(data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            if request.user.is_staff:
                Category.objects.filter(id=pk).update(deleted=datetime.now())
            else:
                Category.objects.filter(id=pk).update(deleted_at=datetime.now())
            return redirect('/tasks/categories/')
    form = CategoryDeleteForm()
    content = {
        'category': Category.objects.get(id=pk),
        'form': form,
    }
    return render(request, 'task/category_delete.html', content)
