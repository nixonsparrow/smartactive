from django.contrib import admin

from payments.models import Payment, Ticket


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'user', 'ticket', 'updated_at', 'created_at']


class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'usages_left', 'user', 'active', 'payment', 'updated_at', 'created_at']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Ticket, TicketAdmin)
