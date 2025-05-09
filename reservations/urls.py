from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewSet, TicketViewSet

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
