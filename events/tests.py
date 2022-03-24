import datetime

from django.test import TestCase
from django.utils.timezone import now

from events.models import Event, Type
from payments.models import Ticket
from users.models import User
from users.tests import PASSWORD, TEST_USER

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
        with self.assertRaises(LookupError):
            self.event.register_user(self.new_user)
        self.assertEqual(self.event.participants.all().count(), 0)

    def test_if_ticket_usages_left_decrease_after_register(self):
        self.assertEqual(self.ticket.usages_left, TEST_TICKET['usages_left'])
        self.event.register_user(self.user)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.usages_left, TEST_TICKET['usages_left'] - 1)

    def test_if_ticket_usages_left_not_decrease_after_failed_register(self):
        self.assertEqual(self.ticket.usages_left, TEST_TICKET['usages_left'])
        with self.assertRaises(LookupError):
            self.event.register_user(self.new_user)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.usages_left, TEST_TICKET['usages_left'])
