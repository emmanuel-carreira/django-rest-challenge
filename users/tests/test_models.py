from django.test import TestCase
from django.utils import timezone

from model_bakery import baker

from users.models import User


class UserModelTests(TestCase):
    def setUp(self):
        self.first_name = 'User'
        self.last_name = 'Tester'
        self.last_login = timezone.now()
        self.user = baker.make(
            User, first_name=self.first_name, last_name=self.last_name,
            last_login=self.last_login
        )

    def test_get_full_name(self):
        """Checks if get_full_name() returns the user's name correctly"""
        full_name = self.user.get_full_name()
        expected_full_name = self.first_name + ' ' + self.last_name
        self.assertEquals(
            full_name,
            expected_full_name,
            msg="""get_full_name() returned incorrect name. Expected: {}.
            Obtained: {}.""".format(expected_full_name, full_name)
        )

    def test_get_short_name(self):
        """Checks if get_short_name() returns the user's first name"""
        first_name = self.user.get_short_name()
        self.assertEquals(
            first_name,
            self.first_name,
            msg="""get_short_name() returned the user's first name incorrectly.
            Expected: {}. Obtained: {}.""".format(self.first_name, first_name)
        )

    def test_update_last_login(self):
        """Checks if update_last_login() updates the user's last_login field"""
        self.user.update_last_login()
        last_login = self.user.last_login
        self.assertGreater(
            last_login,
            self.last_login,
            msg="""update_last_login() did not update the user's last_login
            field correctly."""
        )
