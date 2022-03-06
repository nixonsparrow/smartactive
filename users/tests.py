from django.test import TestCase, Client
from django.shortcuts import reverse
from users.models import User
from users.forms import UserCreateForm, UserUpdateForm


TEST_USER = {
    'username': 'Tester',
    'first_name': 'First Name',
    'last_name': 'Last Name',
    'email': 'test@wp.pl',
}

PASSWORD = 'T3$tuser!@#$%^&*()'


class UserCreationTestCase(TestCase):
    def test_simple_creation(self):
        self.assertEqual(User.objects.all().count(), 0)
        User.objects.create()
        self.assertEqual(User.objects.all().count(), 1)

    def test_user_form_creates_user(self):
        self.assertEqual(User.objects.all().count(), 0)
        data = {**TEST_USER, **{'password1': PASSWORD, 'password2': PASSWORD}}
        new_user = UserCreateForm(data=data)
        new_user.save()

        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.first().username, 'Tester')

    def test_user_form_creates_user_not_trainer(self):
        data = {**TEST_USER, **{'password1': PASSWORD, 'password2': PASSWORD}}
        new_user = UserCreateForm(data=data)
        new_user.save()
        self.assertFalse(User.objects.first().trainer)

    def test_create_view_uses_user_form(self):
        response = self.client.get(reverse('users:create-form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_form.html')

    def test_user_post_creates_user(self):
        response = self.client.post(reverse('users:create-form'),
                                    data={**TEST_USER, **{'password1': PASSWORD, 'password2': PASSWORD}})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.first().username, TEST_USER['username'])


class UserUpdateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username=TEST_USER['username'],
                                                  email=TEST_USER['email'],
                                                  password=PASSWORD)
        self.client.login(username=TEST_USER['email'], password=PASSWORD)

    def test_update_view_uses_user_form(self):
        response = self.client.get(reverse('users:update-form', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_form.html')

    def test_user_post_updates_user(self):
        response = self.client.post(reverse('users:update-form', kwargs={'pk': self.user.id}),
                                    {**TEST_USER, 'username': 'Alternative'})
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, TEST_USER['username'])
