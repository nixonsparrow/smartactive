from django.test import TestCase
from users.models import User
from users.forms import UserCreateForm, UserUpdateForm


TEST_USER = {
    'username': 'Tester',
    'first_name': 'First Name',
    'last_name': 'Last Name',
    'email': 'test@wp.pl',
}


class UserCreationTestCase(TestCase):
    def test_user_form_creates_user(self):
        self.assertEqual(User.objects.all().count(), 0)
        data = {**TEST_USER, **{'password1': 'T3$tuser!@#$%^&*()',
                                'password2': 'T3$tuser!@#$%^&*()'}}
        new_user = UserCreateForm(data=data)
        new_user.save()
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.first().username, 'Tester')

    def test_user_form_creates_user_not_trainer(self):
        data = {**TEST_USER, **{'password1': 'T3$tuser!@#$%^&*()',
                                'password2': 'T3$tuser!@#$%^&*()'}}
        new_user = UserCreateForm(data=data)
        new_user.save()
        self.assertFalse(User.objects.first().trainer)


class UserUpdateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=TEST_USER['username'])

    def test_user_form_updates_user(self):
        self.assertEqual(self.user.username, TEST_USER['username'])
        self.assertEqual(self.user.first_name, '')

        data = {**TEST_USER, **{'username': 'DifferentUsername',
                                'password1': 'T3$tuser!@#$%^&*()',
                                'password2': 'T3$tuser!@#$%^&*()'}}
        print(data)
        new_user = UserUpdateForm()
        new_user.save()

        self.assertNotEqual(self.user.username, TEST_USER['username'])
        self.assertEqual(self.user.first_name, TEST_USER['first_name'])
