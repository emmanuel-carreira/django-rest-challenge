from django.test import TestCase
from rest_framework.exceptions import ValidationError

from model_bakery import baker

from users.constants import MISSING_FIELD_ERROR, EMAIL_ALREADY_REGISTERED_ERROR
from users.models import User, Phone
from users.serializers import PhoneSerializer, UserModelSerializer


class PhoneSerializerTests(TestCase):
    def setUp(self):
        self.number = 987465489
        self.area_code = 81
        self.country_code = '+55'
        self.user = baker.make(User)
        self.phone = baker.make(
            Phone, number=self.number, area_code=self.area_code,
            country_code=self.country_code, user=self.user
        )

    def test_phoneserializer_serialization(self):
        """Checks Phone fields returned by PhoneSerializer"""
        serializer = PhoneSerializer(self.phone)
        phone_data = serializer.data

        for key in ['number', 'area_code', 'country_code']:
            self.assertIn(
                key,
                phone_data.keys(),
                msg="""PhoneSerializer did not return {} information."""
                .format(key)
            )

            value = phone_data[key]
            expected_value = getattr(self.phone, key)
            self.assertEqual(
                value,
                expected_value,
                msg="""PhoneSerializer returned incorrect {} information.
                Expected: {}. Obtained: {}""".format(
                    key, expected_value, value
                )
            )

    def test_phoneserializer_deserialization_missing_field(self):
        """Checks new Phone instance creation using PhoneSerializer

        Test if PhoneSerializer deserialization is invalid due to missing
        mandatory field."""
        data = {
            'number': self.number,
            'area_code': self.area_code
        }
        serializer = PhoneSerializer(data=data)

        self.assertFalse(
            serializer.is_valid(),
            msg="""Phone deserialization should not be valid since the country
            code is missing."""
        )
        self.assertIn(
            'non_field_errors',
            serializer.errors
        )
        self.assertEqual(
            str(serializer.errors.get('non_field_errors')[0]),
            MISSING_FIELD_ERROR
        )

    def test_phoneserializer_deserialization(self):
        """Checks new Phone instance creation using PhoneSerializer"""
        data = {
            'user_id': self.user.id,
            'number': self.number,
            'area_code': self.area_code,
            'country_code': self.country_code
        }
        serializer = PhoneSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            msg="""Phone deserialization should be valid since all mandatory
            fields are present."""
        )

        test_case_message = ('PhoneSerializer should not attempt to create '
                             'Phone instance.')
        with self.assertRaises(ValidationError, msg=test_case_message):
            serializer.save()


class UserModelSerializerTests(TestCase):
    def setUp(self):
        self.email = 'user@tester.com'
        self.second_email = 'test@tester.com'
        self.first_name = 'User'
        self.last_name = 'Tester'
        self.password = 'test'
        self.phone = {
            'number': 987465489,
            'area_code': 81,
            'country_code': '+55'
        }
        self.data = {
            'email': self.second_email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password,
            'phones': [self.phone]
        }

        self.user = baker.make(
            User, email=self.email, first_name=self.first_name,
            last_name=self.last_name
        )
        self.phone_instance = baker.make(Phone, user=self.user, **self.phone)

    def test_usermodelserializer_serialization(self):
        """Checks User fields returned by UserModelSerializer"""
        serializer = UserModelSerializer(self.user)
        user_data = serializer.data

        for key in ['email', 'first_name', 'last_name']:
            self.assertIn(
                key,
                user_data.keys(),
                msg="""UserModelSerializer did not return {} information."""
                .format(key)
            )

            value = user_data[key]
            expected_value = getattr(self.user, key)
            self.assertEqual(
                value,
                expected_value,
                msg="""UserModelSerializer returned incorrect {} information.
                Expected: {}. Obtained: {}""".format(
                    key, expected_value, value
                )
            )

        user_phone = user_data.get('phones')
        self.assertEqual(
            len(user_phone),
            1,
            msg="""User has only one phone. However, UserModelSerializer
            returned {} phones.""".format(len(user_phone))
        )

        user_phone = user_phone[0]
        for key in ['number', 'area_code', 'country_code']:
            self.assertIn(
                key,
                user_phone.keys(),
                msg="""UserModelSerializer did not return {} information."""
                .format(key)
            )

            value = user_phone[key]
            expected_value = getattr(self.phone_instance, key)
            self.assertEqual(
                value,
                expected_value,
                msg="""UserModelSerializer returned incorrect {} information.
                Expected: {}. Obtained: {}""".format(
                    key, expected_value, value
                )
            )

    def test_usermodelserializer_deserialization_missing_field(self):
        """Checks new User instance creation using UserModelSerializer

        Test if UserModelSerializer deserialization is invalid due to missing
        mandatory field."""
        data = self.data
        data.pop('phones')
        serializer = UserModelSerializer(data=data)

        self.assertFalse(
            serializer.is_valid(),
            msg="""User deserialization should not be valid since the phones
            field is missing."""
        )
        self.assertIn(
            'non_field_errors',
            serializer.errors
        )
        self.assertEqual(
            str(serializer.errors.get('non_field_errors')[0]),
            MISSING_FIELD_ERROR
        )

    def test_usermodelserializer_deserialization_existing_email(self):
        """Checks new User instance creation using UserModelSerializer

        Test if UserModelSerializer deserialization is invalid due to e-mail
        already in database."""
        data = self.data
        data['email'] = self.email
        serializer = UserModelSerializer(data=data)

        self.assertFalse(
            serializer.is_valid(),
            msg="""User deserialization should not be valid since the e-mail
            already exists in the database."""
        )
        self.assertIn(
            'non_field_errors',
            serializer.errors
        )
        self.assertEqual(
            str(serializer.errors.get('non_field_errors')[0]),
            EMAIL_ALREADY_REGISTERED_ERROR
        )

    def test_usermodelserializer_deserialization(self):
        """Checks new User instance creation using UserModelSerializer"""
        serializer = UserModelSerializer(data=self.data)

        self.assertTrue(
            serializer.is_valid(),
            msg="""User deserialization should be valid since all mandatory
            fields are present."""
        )

    def test_usermodelserializer_update_not_allowed(self):
        """Checks User instance update using UserModelSerializer

        Tests if UserModelSerializer update is invalid due to update not
        allowed."""
        serializer = UserModelSerializer(self.user, data=self.data)
        serializer.is_valid()

        test_case_message = ('UserModelSerializer should not attempt to update'
                             ' User instance.')
        with self.assertRaises(ValidationError, msg=test_case_message):
            serializer.save()
