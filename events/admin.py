from django.contrib import admin

from events.models import Event, EventSchema, Type


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class EventSchemaAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Event, EventAdmin)
admin.site.register(EventSchema, EventSchemaAdmin)
admin.site.register(Type, TypeAdmin)
