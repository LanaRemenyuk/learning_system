from django.urls import include, path

from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, LessonViewSet, WatchedViewSet, ProductViewSet, get_stat

app_name = 'api'

router = routers.DefaultRouter()
router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('lessons', LessonViewSet, basename='lessons')
router_v1.register('products', ProductViewSet, basename='products')
router_v1.register('lessons_watched', WatchedViewSet, basename='lessons_watched')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('stats/', get_stat, name='stats')
]