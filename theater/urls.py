from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TheatreHallViewSet,
    ActorViewSet,
    GenreViewSet,
    PlayViewSet,
    PerformanceViewSet
)

router = DefaultRouter()
router.register(r'theatre_halls', TheatreHallViewSet)
router.register(r'actors', ActorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'plays', PlayViewSet)
router.register(r'performances', PerformanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
