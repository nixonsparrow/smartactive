from django.contrib import admin

from payments.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'user', 'updated_at', 'created_at']


admin.site.register(Payment, PaymentAdmin)
