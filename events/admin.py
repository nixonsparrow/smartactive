from django.contrib import admin

from events.models import Event, EventRegistration, EventSchema, Ticket, Type


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class EventSchemaAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'direction', 'user', 'event', 'updated_at', 'created_at']


class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'usages_left', 'user', 'active', 'payment', 'event_type', 'updated_at', 'created_at']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Event, EventAdmin)
admin.site.register(EventSchema, EventSchemaAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Ticket, TicketAdmin)
