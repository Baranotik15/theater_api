from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

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

    @extend_schema(
        request=TicketSerializer,
        responses={
            201: TicketSerializer,
            400: OpenApiResponse(
                description="Bad Request: Invalid data"
            ),
        },
        operation_id="create_ticket",
        description="Create a new ticket for the "
                    "authenticated user's reservation.",
    )
    def perform_create(self, serializer):
        with transaction.atomic():
            ticket = Ticket(**serializer.validated_data)
            try:
                ticket.clean()
            except ValidationError as e:
                raise ValidationError(e.message_dict)
            serializer.save()

    @extend_schema(
        responses={
            200: TicketSerializer,
            403: OpenApiResponse(
                description="Forbidden: You do not have "
                            "permission to view this ticket."
            ),
        },
        operation_id="get_ticket",
        description="Retrieve a specific ticket for the "
                    "logged-in user. Only tickets related "
                    "to the authenticated user are allowed.",
    )
    def retrieve(self, request, *args, **kwargs):
        ticket = self.get_object()
        if ticket.reservation.user != request.user:
            return Response(
                {
                    "detail": "You do not have permission to view this ticket."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        return super().retrieve(request, *args, **kwargs)
