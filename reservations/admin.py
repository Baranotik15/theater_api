from django.contrib import admin
from .models import Reservation, Ticket
from theater.models import Performance


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at',)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'performance', 'reservation', 'row', 'seat')
    search_fields = ('performance__title', 'reservation__user__username')
    list_filter = ('performance', 'reservation__user')

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Ticket, TicketAdmin)
