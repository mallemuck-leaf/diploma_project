from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('create/', views.task_create, name='task_create'),
    path('update/<int:pk>', views.task_update, name='task_update'),
    path('delete/<int:pk>', views.task_delete, name='task_delete'),
    path('deleted/', views.deleted_task_list, name='deleted_task_list'),
    path('deleted/<int:pk>', views.deleted_task_recovery, name='deleted_task_recovery'),
    path('deleted/priorities/', views.deleted_priority_list, name='deleted_priority_list'),
    path('deleted/priorities/<int:pk>', views.deleted_priority_recovery, name='deleted_priority_recovery'),
    path('deleted/categories/', views.deleted_category_list, name='deleted_category_list'),
    path('deleted/categories/<int:pk>', views.deleted_category_recovery, name='deleted_category_recovery'),
    path('priorities/', views.priority_list, name='priority_list'),
    path('priorities/priority/<int:pk>', views.priority_update, name='priority_update'),
    path('priorities/delete/<int:pk>', views.priority_delete, name='priority_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/category/<int:pk>', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>', views.category_delete, name='category_delete'),
]
