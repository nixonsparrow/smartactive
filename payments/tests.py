from django.shortcuts import reverse
from django.test import TestCase

from events.models import Type
from payments.forms import PaymentForm
from payments.models import Payment, Ticket
from users.models import User
from users.tests import PASSWORD, TEST_SUPERUSER, TEST_USER

TEST_PAYMENT = {
    'initial_usages': 1,
    'amount': 29,
}


class PaymentCreationTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username=TEST_SUPERUSER['username'],
            email=TEST_SUPERUSER['email'],
            password=PASSWORD)

        self.user = User.objects.create_user(
            username=TEST_USER['username'],
            email=TEST_USER['email'],
            password=PASSWORD)

    def test_payment_form_creates_payment(self):
        self.assertEqual(Payment.objects.all().count(), 0)
        data = {**TEST_PAYMENT}
        new_payment = PaymentForm(data=data)
        new_payment.save()

        self.assertEqual(Payment.objects.all().count(), 1)
        self.assertEqual(Payment.objects.first().amount, TEST_PAYMENT['amount'])

    def test_create_view_uses_payment_form(self):
        self.client.login(username=self.superuser.email, password=PASSWORD)
        response = self.client.get(reverse('payments:new'))
        self.assertTemplateUsed(response, 'payments/payment_form.html')

    def test_create_view_anonymous_user_redirect(self):
        response = self.client.get(reverse('payments:new'))
        self.assertEqual(response.status_code, 302)

    def test_create_view_common_user_forbidden(self):
        self.client.login(username=self.user.email, password=PASSWORD)
        response = self.client.get(reverse('payments:new'))
        self.assertEqual(response.status_code, 403)

    def test_create_view_admin_user_no_redirect(self):
        self.client.login(username=self.superuser.email, password=PASSWORD)
        response = self.client.get(reverse('payments:new'))
        self.assertEqual(response.status_code, 200)

    def test_post_creates_payment_object_and_redirects(self):
        self.assertEqual(Payment.objects.all().count(), 0)
        self.client.login(username=self.superuser.email, password=PASSWORD)
        response = self.client.post(reverse('payments:new'), data={**TEST_PAYMENT})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Payment.objects.all().count(), 1)

    def test_post_creates_proper_values(self):
        self.client.login(username=self.superuser.email, password=PASSWORD)
        self.client.post(reverse('payments:new'), data={**TEST_PAYMENT})
        payment = Payment.objects.last()
        self.assertEqual((payment.initial_usages, payment.amount),
                         (TEST_PAYMENT['initial_usages'], TEST_PAYMENT['amount']))


class PaymentCreationSignalTicketTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username=TEST_SUPERUSER['username'],
            email=TEST_SUPERUSER['email'],
            password=PASSWORD)
        self.client.login(username=self.superuser.email, password=PASSWORD)
        self.event_type = Type.objects.create(name='TestType')

    def test_payment_created_initiates_ticket_creation(self):
        self.assertEqual(Ticket.objects.all().count(), 0)
        self.client.post(reverse('payments:new'), data={**TEST_PAYMENT})
        self.assertEqual(Ticket.objects.all().count(), 1)

    def test_payment_created_passes_user_to_ticket(self):
        self.client.post(reverse('payments:new'), data={**TEST_PAYMENT, **{'user': self.superuser.id}})
        self.assertEqual(Ticket.objects.last().user, self.superuser)

    def test_payment_created_passes_event_type_to_ticket(self):
        self.client.post(reverse('payments:new'), data={**TEST_PAYMENT, **{'event_type': self.event_type.id}})
        self.assertEqual(Ticket.objects.last().event_type.name, 'TestType')

    def test_payment_created_has_relation_to_new_ticket(self):
        self.client.post(reverse('payments:new'), data={**TEST_PAYMENT})
        self.assertEqual(Ticket.objects.last(), Payment.objects.last().ticket)

# TODO make more tests
