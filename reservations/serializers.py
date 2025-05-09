from rest_framework import serializers
from .models import Reservation, Ticket
from theater.models import Performance
from django.contrib.auth import get_user_model


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'row', 'seat', 'performance', 'reservation']

class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'created_at', 'user', 'tickets']
