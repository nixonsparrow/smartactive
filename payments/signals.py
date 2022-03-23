from django.db.models.signals import post_save
from django.dispatch import receiver

from payments.models import Payment, Ticket


@receiver(post_save, sender=Payment)
def create_ticket(sender, instance, created, **kwargs):
    if created:
        instance.ticket = Ticket.objects.create(
            user=instance.user,
            usages_left=instance.initial_usages,
            event_type=instance.event_type,
        )
        instance.save()
