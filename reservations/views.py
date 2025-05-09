from rest_framework import viewsets
from .models import Ticket
from .serializers import TicketSerializer
from rest_framework.permissions import IsAuthenticated


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(
            reservation__user=self.request.user
        ).select_related('reservation')

    def perform_create(self, serializer):
        serializer.save()
