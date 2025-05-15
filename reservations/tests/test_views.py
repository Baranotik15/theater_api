from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from theater.models import TheatreHall, Play, Performance
from reservations.models import Ticket, Reservation


User = get_user_model()


class TicketViewSetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            username="testuser"
        )
        self.client = APIClient()
        self.client.force_authenticate(
            user=self.user
        )

        self.theatre_hall = TheatreHall.objects.create(
            name="Main Hall",
            rows=10,
            seats_in_row=20,
            capacity=200
        )
        self.play = Play.objects.create(
            title="Hamlet",
            description="Shakespeare's masterpiece"
        )
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time="2024-03-20T19:00:00Z",
        )
        self.reservation = Reservation.objects.create(
            user=self.user,
            performance=self.performance
        )

    def test_create_ticket(self):
        """Test creating a ticket"""
        data = {
            "reservation": self.reservation.id,
            "row": 5,
            "seat": 10
        }
        response = self.client.post(
            reverse("ticket-list"),
            data,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Ticket.objects.count(),
            1
        )
        ticket = Ticket.objects.first()
        self.assertEqual(
            ticket.row,
            5
        )
        self.assertEqual(
            ticket.seat,
            10
        )

    def test_list_user_tickets(self):
        """Test listing user's tickets"""
        Ticket.objects.create(
            reservation=self.reservation,
            row=1,
            seat=1
        )
        Ticket.objects.create(
            reservation=self.reservation,
            row=1,
            seat=2
        )

        response = self.client.get(
            reverse("ticket-list")
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["count"],
            2
        )
        self.assertEqual(
            len(response.data["results"]),
            2
        )

    def test_retrieve_own_ticket(self):
        """Test retrieving own ticket"""
        ticket = Ticket.objects.create(
            reservation=self.reservation,
            row=1,
            seat=1
        )
        response = self.client.get(
            reverse(
                "ticket-detail",
                kwargs={"pk": ticket.id}
            )
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["row"],
            1
        )

    def test_retrieve_other_user_ticket(self):
        """Test retrieving another user's ticket"""
        other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass123",
            username="otheruser"
        )
        other_reservation = Reservation.objects.create(
            user=other_user,
            performance=self.performance
        )
        other_ticket = Ticket.objects.create(
            reservation=other_reservation,
            row=2,
            seat=2
        )

        response = self.client.get(
            reverse(
                "ticket-detail",
                kwargs={"pk": other_ticket.id}
            )
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_create_ticket_invalid_seat(self):
        """Test creating a ticket with invalid seat number"""
        data = {
            "reservation": self.reservation.id,
            "row": 5,
            "seat": 25
        }
        response = self.client.post(
            reverse("ticket-list"),
            data,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            Ticket.objects.count(),
            0
        )

    def test_create_ticket_invalid_row(self):
        """Test creating a ticket with invalid row number"""
        data = {
            "reservation": self.reservation.id,
            "row": 15,
            "seat": 10
        }
        response = self.client.post(
            reverse("ticket-list"),
            data,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            Ticket.objects.count(),
            0
        )

    def test_create_duplicate_ticket(self):
        """Test creating a ticket for already reserved seat"""
        Ticket.objects.create(
            reservation=self.reservation,
            row=5,
            seat=10
        )

        data = {
            "reservation": self.reservation.id,
            "row": 5,
            "seat": 10
        }
        response = self.client.post(
            reverse("ticket-list"),
            data,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            Ticket.objects.count(),
            1
        )

    def test_list_tickets_unauthenticated(self):
        """Test listing tickets without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(
            reverse("ticket-list")
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_get_nonexistent_ticket(self):
        """Test getting a non-existent ticket"""
        response = self.client.get(
            reverse(
                "ticket-detail",
                kwargs={"pk": 99999}
            )
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
