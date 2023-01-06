# Imports
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import UserView
router = SimpleRouter()
router = DefaultRouter()
router.register('users', UserView, basename='users')


urlpatterns = router.urls