from rest_framework import serializers
from theater.models import (
    TheatreHall,
    Actor,
    Genre,
    Play,
    Performance
)


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ['id', 'name', 'rows', 'seats_in_row']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'first_name', 'last_name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ['id', 'title', 'description']


class PerformanceSerializer(serializers.ModelSerializer):
    play = serializers.PrimaryKeyRelatedField(queryset=Play.objects.all())
    theatre_hall = serializers.PrimaryKeyRelatedField(queryset=TheatreHall.objects.all())

    class Meta:
        model = Performance
        fields = ['id', 'play', 'theatre_hall', 'show_time']
