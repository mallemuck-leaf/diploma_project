from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'persons', views.PersonViewSet, basename='person')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'priorities', views.PriorityViewSet, basename='priority')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'recovery/categories', views.CategoryViewSet, basename='recovery_category')
router.register(r'recovery/priorities', views.RecoveryPriorityViewSet, basename='recovery_priority')
router.register(r'recovery/tasks', views.TaskViewSet, basename='recovery_task')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_framework.urls')),
]
