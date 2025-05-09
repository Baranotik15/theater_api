from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'performance', 'reservation', 'row', 'seat')
    search_fields = ('performance__title',)
    list_filter = ('performance',)
    readonly_fields = ('performance',)

    def save_model(self, request, obj, form, change):
        obj.clean()
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('reservation',)
        return self.readonly_fields
