from rest_framework import serializers
from reservations.models import Reservation, Ticket


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user"]
        read_only_fields = ["id", "created_at"]


class TicketSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(required=False)

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance", "reservation"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        data = super().validate(attrs)

        performance = attrs["performance"]
        seat = attrs["seat"]
        row = attrs["row"]

        Ticket.validate_seat(seat, row, performance)
        Ticket.validate_row(row, performance)

        return data

    def create(self, validated_data):
        reservation_data = validated_data.pop("reservation", None)
        if reservation_data is None:
            reservation = Reservation.objects.create(
                user=self.context["request"].user
            )
        else:
            reservation = Reservation.objects.create(
                user=reservation_data["user"]
            )
        ticket = Ticket.objects.create(
            reservation=reservation, **validated_data
        )
        return ticket
