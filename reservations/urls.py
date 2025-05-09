from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reservations.views import TicketViewSet

router = DefaultRouter()
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
