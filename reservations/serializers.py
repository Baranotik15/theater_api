from rest_framework import serializers
from .models import Reservation, Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'row', 'seat', 'performance', 'reservation']


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'created_at', 'user', 'tickets']
