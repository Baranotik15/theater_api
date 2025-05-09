from django.db import transaction
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

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
        with transaction.atomic():
            ticket = Ticket(**serializer.validated_data)
            try:
                ticket.clean()
            except ValidationError as e:
                raise ValidationError(e.message_dict)
            serializer.save()
