from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from theater.models import TheatreHall, Play, Performance, Genre


class TheaterViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.theatre_hall = TheatreHall.objects.create(
            name="Main Hall",
            rows=10,
            seats_in_row=20,
            capacity=200
        )
        self.genre = Genre.objects.create(
            name="Drama"
        )
        self.play = Play.objects.create(
            title="Hamlet",
            description="Shakespeare's masterpiece"
        )
        self.play.genres.add(self.genre)
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time="2024-03-20T19:00:00Z",
        )

    def test_theatre_hall_list(self):
        """Test getting list of theatre halls"""
        response = self.client.get(
            reverse("theatrehall-list")
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["count"],
            1
        )
        self.assertEqual(
            len(response.data["results"]),
            1
        )
        self.assertEqual(
            response.data["results"][0]["name"],
            "Main Hall"
        )

    def test_create_theatre_hall(self):
        """Test creating a new theatre hall"""
        data = {
            "name": "New Hall",
            "rows": 15,
            "seats_in_row": 25,
            "capacity": 375
        }
        response = self.client.post(
            reverse("theatrehall-list"),
            data,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            TheatreHall.objects.count(),
            2
        )
        self.assertEqual(
            TheatreHall.objects.last().name,
            "New Hall"
        )

    def test_play_detail(self):
        """Test getting play details"""
        response = self.client.get(
            reverse(
                "play-detail",
                kwargs={"pk": self.play.id}
            )
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["title"],
            "Hamlet"
        )
        self.assertEqual(
            response.data["description"],
            "Shakespeare's masterpiece"
        )

    def test_create_performance(self):
        """Test creating a new performance"""
        data = {
            "play": self.play.id,
            "theatre_hall": self.theatre_hall.id,
            "show_time": "2024-03-21T19:00:00Z",
        }
        response = self.client.post(
            reverse("performance-list"),
            data,
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Performance.objects.count(),
            2
        )
        self.assertEqual(
            Performance.objects.last().show_time.isoformat(),
            "2024-03-21T19:00:00+00:00",
        )

    def test_play_list(self):
        """Test getting list of plays"""
        response = self.client.get(reverse("play-list"))
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["count"],
            1
        )
        self.assertEqual(
            len(response.data["results"]),
            1
        )
        self.assertEqual(
            response.data["results"][0]["title"],
            "Hamlet"
        )

    def test_performance_detail(self):
        """Test getting performance details"""
        response = self.client.get(
            reverse(
                "performance-detail",
                kwargs={"pk": self.performance.id}
            )
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["play"],
            self.play.id
        )
        self.assertEqual(
            response.data["theatre_hall"],
            self.theatre_hall.id
        )
