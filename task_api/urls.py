from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'persons', views.PersonViewSet, basename='person')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'priorities', views.PriorityViewSet, basename='priority')
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_framework.urls')),
]
