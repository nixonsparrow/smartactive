import datetime

from dateutil.utils import today
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from events.exceptions import (NoValidTicketFound, ParticipantsFull,
                               RegisterTimePassed, UnregisterTimePassed,
                               UserInParticipants, UserNotInParticipants)
from events.models import Event, EventRegistration, Ticket, Type
from users.models import User
from users.tests import PASSWORD, TEST_SUPERUSER, TEST_USER

TEST_TYPE = {
    'name': 'Test Type'
}

TEST_EVENT = {
    'title': 'Test Title',
    'time': datetime.time(hour=18, minute=00),
    'date': now() + datetime.timedelta(days=1)
}

TEST_TICKET = {
    'usages_left': 4
}


class OverviewTestCase(TestCase):
    def setUp(self):
        self.type = Type.objects.create(name=TEST_TYPE['name'])
        self.event = Event.objects.create(title=TEST_EVENT['title'],
                                          type=self.type,
                                          date=TEST_EVENT['date'],
                                          time=TEST_EVENT['time'])

    def test_calendar_overview_template_used(self):
        response = self.client.get(reverse('calendar:overview'))
        self.assertTemplateUsed(response, 'events/payment_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_calendar_overview_anonymous_user_see_page(self):
        response = self.client.get(reverse('calendar:overview'))
        self.assertEqual(response.status_code, 200)


class RegisterTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USER['username'],
            email=TEST_USER['email'],
            password=PASSWORD)

        self.new_user = User.objects.create_user(
            username=TEST_USER['username']+'TEST',
            email=TEST_USER['email']+'+TEST',
            password=PASSWORD)

        self.type = Type.objects.create(name=TEST_TYPE['name'])
        self.ticket = Ticket.objects.create(user=self.user,
                                            event_type=self.type,
                                            usages_left=TEST_TICKET['usages_left'])
        self.event = Event.objects.create(title=TEST_EVENT['title'],
                                          type=self.type,
                                          date=TEST_EVENT['date'],
                                          time=TEST_EVENT['time'])

    def test_if_user_with_valid_ticket_can_register_to_event(self):
        self.assertEqual(self.event.participants.all().count(), 0)
        self.event.register_user(self.user)
        self.assertEqual(self.event.participants.all().count(), 1)
        self.assertIn(self.user, self.event.participants.all())

    def test_if_user_without_valid_ticket_cannot_register_to_event(self):
        self.assertEqual(self.event.participants.all().count(), 0)
        with self.assertRaises(NoValidTicketFound):
            self.event.register_user(self.new_user)
        self.assertEqual(self.event.participants.all().count(), 0)

    def test_if_ticket_usages_left_decrease_after_register(self):
        self.assertEqual(self.ticket.usages_left, TEST_TICKET['usages_left'])
        self.event.register_user(self.user)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.usages_left, TEST_TICKET['usages_left'] - 1)

    def test_if_ticket_usages_left_not_decrease_after_failed_register(self):
        self.assertEqual(self.ticket.usages_left, TEST_TICKET['usages_left'])
        with self.assertRaises(NoValidTicketFound):
            self.event.register_user(self.new_user)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.usages_left, TEST_TICKET['usages_left'])

    def test_if_event_registration_created_after_register(self):
        self.assertEqual(EventRegistration.objects.count(), 0)
        self.event.register_user(self.user)
        self.assertEqual(EventRegistration.objects.count(), 1)

    def test_if_event_registration_created_with_proper_user_after_register(self):
        self.event.register_user(self.user)
        self.assertEqual(EventRegistration.objects.last().user, self.user)

    def test_if_event_registration_created_with_proper_ticket_after_register(self):
        self.event.register_user(self.user)
        self.assertEqual(EventRegistration.objects.last().ticket, self.ticket)

    def test_if_event_registration_created_with_proper_ticket_usages_left_after_register(self):
        wanted_usages = self.ticket.usages_left - 1
        self.event.register_user(self.user)
        self.assertEqual(EventRegistration.objects.last().ticket.usages_left, wanted_usages)

    def test_if_event_registration_created_with_proper_event_after_register(self):
        self.event.register_user(self.user)
        self.assertEqual(EventRegistration.objects.last().event, self.event)

    def test_if_event_registration_created_with_proper_direction_after_register(self):
        self.event.register_user(self.user)
        self.assertEqual(EventRegistration.objects.last().direction, 1)


class CannotRegisterTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USER['username'],
            email=TEST_USER['email'],
            password=PASSWORD)

        self.new_user = User.objects.create_user(
            username=TEST_USER['username'] + 'TEST',
            email=TEST_USER['email'] + '+TEST',
            password=PASSWORD)

        self.event_type = Type.objects.create(name=TEST_TYPE['name'])
        self.ticket = Ticket.objects.create(user=self.user,
                                            event_type=self.event_type,
                                            usages_left=TEST_TICKET['usages_left'])
        self.event = Event.objects.create(title=TEST_EVENT['title'],
                                          type=self.event_type,
                                          date=TEST_EVENT['date'],
                                          time=TEST_EVENT['time'])

    def test_if_user_cannot_register_while_already_participating(self):
        self.event.participants.add(self.user)
        with self.assertRaises(UserInParticipants):
            self.event.register_user(self.user)

    def test_if_user_cannot_register_if_participants_limit_reached(self):
        self.event.participants_limit = 0
        with self.assertRaises(ParticipantsFull):
            self.event.register_user(self.user)

    def test_if_user_cannot_register_with_ticket_without_usages_left(self):
        self.ticket = Ticket.objects.create(user=self.new_user,
                                            event_type=self.event_type,
                                            usages_left=0)
        with self.assertRaises(NoValidTicketFound):
            self.event.register_user(self.new_user)

    def test_if_user_cannot_register_after_register_time_limit(self):
        event = Event.objects.create(title=TEST_EVENT['title'], date=today(), type=self.event_type,
                                     time=(datetime.datetime.now() + datetime.timedelta(minutes=60)).time(),
                                     register_time_limit=61)
        with self.assertRaises(RegisterTimePassed):
            event.register_user(self.user)


class UnregisterTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USER['username'],
            email=TEST_USER['email'],
            password=PASSWORD)

        self.new_user = User.objects.create_user(
            username=TEST_USER['username'] + 'TEST',
            email=TEST_USER['email'] + '+TEST',
            password=PASSWORD)

        self.event_type = Type.objects.create(name=TEST_TYPE['name'])
        self.ticket = Ticket.objects.create(user=self.user,
                                            event_type=self.event_type,
                                            usages_left=TEST_TICKET['usages_left'])
        self.event = Event.objects.create(title=TEST_EVENT['title'],
                                          type=self.event_type,
                                          date=TEST_EVENT['date'],
                                          time=TEST_EVENT['time'])

    def test_if_event_registration_created_after_unregister(self):
        self.event.register_user(self.user)
        self.assertEqual(EventRegistration.objects.count(), 1)
        self.event.unregister_user(self.user)
        self.assertEqual(EventRegistration.objects.count(), 2)

    def test_if_event_registration_created_with_proper_user_after_unregister(self):
        self.event.participants.add(self.user)
        self.event.unregister_user(self.user)
        self.assertEqual(EventRegistration.objects.last().user, self.user)

    def test_if_event_registration_created_with_proper_ticket_after_unregister(self):
        self.event.participants.add(self.user)
        self.event.unregister_user(self.user)
        self.assertEqual(EventRegistration.objects.last().ticket, self.ticket)

    def test_if_event_registration_created_with_proper_ticket_usages_left_after_unregister(self):
        wanted_usages = self.ticket.usages_left + 1
        self.event.participants.add(self.user)
        self.event.unregister_user(self.user)
        self.assertEqual(EventRegistration.objects.last().ticket.usages_left, wanted_usages)

    def test_if_event_registration_created_with_proper_event_after_unregister(self):
        self.event.participants.add(self.user)
        self.event.unregister_user(self.user)
        self.assertEqual(EventRegistration.objects.last().event, self.event)

    def test_if_event_registration_created_with_proper_direction_after_unregister(self):
        self.event.participants.add(self.user)
        self.event.unregister_user(self.user)
        self.assertEqual(EventRegistration.objects.last().direction, -1)

    def test_if_proper_ticket_gets_usage_after_unregister(self):
        wanted_usages = self.ticket.usages_left + 1
        self.event.participants.add(self.user)
        self.event.unregister_user(self.user)
        ticket = self.user.get_ticket(self.event.type)
        self.assertEqual(ticket.usages_left, wanted_usages)


class CannotUnregisterTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USER['username'],
            email=TEST_USER['email'],
            password=PASSWORD)

        self.new_user = User.objects.create_user(
            username=TEST_USER['username'] + 'TEST',
            email=TEST_USER['email'] + '+TEST',
            password=PASSWORD)

        self.event_type = Type.objects.create(name=TEST_TYPE['name'])
        self.ticket = Ticket.objects.create(user=self.user,
                                            event_type=self.event_type,
                                            usages_left=TEST_TICKET['usages_left'])
        self.event = Event.objects.create(title=TEST_EVENT['title'],
                                          type=self.event_type,
                                          date=TEST_EVENT['date'],
                                          time=TEST_EVENT['time'])

    def test_if_user_cannot_unregister_after_unregister_time_limit(self):
        event = Event.objects.create(title=TEST_EVENT['title'], date=today(), type=self.event_type,
                                     time=(datetime.datetime.now() + datetime.timedelta(minutes=60)).time(),
                                     unregister_time_limit=60)
        event.participants.add(self.user)
        with self.assertRaises(UnregisterTimePassed):
            event.unregister_user(self.user)

    def test_if_user_cannot_unregister_while_not_participating(self):
        with self.assertRaises(UserNotInParticipants):
            self.event.unregister_user(self.user)


class EventDetailViewTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username=TEST_SUPERUSER['username'],
            email=TEST_SUPERUSER['email'],
            password=PASSWORD)

        self.user = User.objects.create_user(
            username=TEST_USER['username'],
            email=TEST_USER['email'],
            password=PASSWORD)

        self.event_type = Type.objects.create(name=TEST_TYPE['name'])
        self.ticket = Ticket.objects.create(user=self.user,
                                            event_type=self.event_type,
                                            usages_left=TEST_TICKET['usages_left'])
        self.event = Event.objects.create(title=TEST_EVENT['title'],
                                          type=self.event_type,
                                          date=TEST_EVENT['date'],
                                          time=TEST_EVENT['time'])

    def test_detail_view_template_used(self):
        response = self.client.get(reverse('calendar:event-detail', kwargs={'pk': self.event.id}))
        self.assertTemplateUsed(response, 'events/event_detail.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_detail_view_anonymous_user_see_page(self):
        response = self.client.get(reverse('calendar:event-detail', kwargs={'pk': self.event.id}))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_wrong_id_404(self):
        response = self.client.get(reverse('calendar:event-detail', kwargs={'pk': self.event.id + 1}))
        self.assertEqual(response.status_code, 404)

    def test_something(self):
        pass
