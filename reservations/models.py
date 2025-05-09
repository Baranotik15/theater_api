from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from theater.models import Performance


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"Reservation by "
            f"{self.user.username} on {self.created_at}"
        )


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('performance', 'row', 'seat')

    def clean(self):
        if Ticket.objects.filter(
                performance=self.performance,
                row=self.row,
                seat=self.seat
        ).exists():
            raise ValidationError(
                "This seat is already reserved for this performance."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Ticket for "
            f"{self.performance.title} at Row "
            f"{self.row}, Seat {self.seat}"
        )
