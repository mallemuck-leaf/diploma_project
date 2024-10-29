from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('create/', views.task_create, name='task_create'),
    path('update/<int:pk>', views.task_update, name='task_update'),
    path('delete/<int:pk>', views.task_delete, name='task_delete'),
    path('priorities/', views.priority_list, name='priority_list'),
    path('priorities/priority/<int:pk>', views.priority_update, name='priority_update'),
    path('priorities/delete/<int:pk>', views.priority_delete, name='priority_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/category/<int:pk>', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>', views.category_delete, name='category_delete'),
]
