from django.test import TestCase
from rest_framework.exceptions import ValidationError

from model_bakery import baker

from users.constants import MISSING_FIELD_ERORR
from users.models import User, Phone
from users.serializers import PhoneSerializer


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
        """Checks phone fields returned by PhoneSerializer"""
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
            MISSING_FIELD_ERORR
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
