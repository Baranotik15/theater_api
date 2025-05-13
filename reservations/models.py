from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from theater.models import Performance


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation by " f"{self.user.username} on {self.created_at}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("performance", "row", "seat")

    @staticmethod
    def validate_row(row, performance):
        hall = performance.theatre_hall
        if not (1 <= row <= hall.rows):
            raise ValidationError(
                f"Row number must be between 1 and {hall.rows}."
            )

    @staticmethod
    def validate_seat(seat, row, performance):
        hall = performance.theatre_hall
        if not (1 <= seat <= hall.seats_in_row):
            raise ValidationError(
                f"Seat number must be between 1 and {hall.seats_in_row}."
            )

    def clean(self):
        Ticket.validate_row(self.row, self.performance)
        Ticket.validate_seat(self.seat, self.row, self.performance)

        if (
            Ticket.objects.filter(
                performance=self.performance, row=self.row, seat=self.seat
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                "This seat is already reserved for this performance."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Ticket for {self.performance.play} at "
            f"Row {self.row}, Seat {self.seat}"
        )
