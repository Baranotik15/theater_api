from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reservations.models import Ticket
from reservations.serializers import TicketSerializer
from reservations.schemas import create_ticket_schema, retrieve_ticket_schema


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(
            reservation__user=self.request.user
        ).select_related("reservation")

    @create_ticket_schema
    def perform_create(self, serializer):
        with transaction.atomic():
            ticket = Ticket(**serializer.validated_data)
            try:
                ticket.clean()
            except ValidationError as e:
                raise ValidationError(e.message_dict)
            serializer.save()

    @retrieve_ticket_schema
    def retrieve(self, request, *args, **kwargs):
        ticket = self.get_object()
        if ticket.reservation.user != request.user:
            return Response(
                {"detail": "You do not have permission to view this ticket."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().retrieve(request, *args, **kwargs)
