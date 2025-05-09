from django.contrib import admin
from .models import (
    TheatreHall,
    Actor,
    Genre,
    Play,
    Performance
)


class TheatreHallAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rows', 'seats_in_row')
    search_fields = ('name',)
    list_filter = ('name',)

class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    list_filter = ('first_name', 'last_name')

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class PlayAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('title',)
    list_filter = ('title',)

class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'play', 'theatre_hall', 'show_time')
    search_fields = ('play', 'theatre_hall')
    list_filter = ('play', 'theatre_hall')

admin.site.register(TheatreHall, TheatreHallAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Play, PlayAdmin)
admin.site.register(Performance, PerformanceAdmin)
