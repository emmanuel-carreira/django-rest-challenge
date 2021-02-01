from django.core.validators import EmailValidator
from rest_framework import serializers

from .constants import (
    MISSING_FIELD_ERROR, EMAIL_ALREADY_REGISTERED_ERROR, INVALID_LOGIN_ERROR
)
from .models import User, Phone
from .utils import get_token_for_user, format_data


class PhoneSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(max_value=2147483647, required=False)
    area_code = serializers.IntegerField(max_value=32767, required=False)
    country_code = serializers.CharField(max_length=4, required=False)

    class Meta:
        model = Phone
        exclude = ['user']

    def create(self, validated_data):
        raise serializers.ValidationError('Create not allowed')

    def update(self, instance, validated_data):
        raise serializers.ValidationError('Update not allowed')

    def validate(self, data):
        number = data.get('number')
        area_code = data.get('area_code')
        country_code = data.get('country_code')

        if not (number and area_code and country_code):
            raise serializers.ValidationError(MISSING_FIELD_ERROR)

        return data


class UserModelSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        max_length=50, required=False, allow_blank=True
    )
    last_name = serializers.CharField(
        max_length=50, required=False, allow_blank=True
    )
    email = serializers.EmailField(required=False)
    password = serializers.CharField(
        max_length=255, write_only=True, required=False, allow_blank=True
    )
    created_at = serializers.DateTimeField(
        required=False, format='%Y-%m-%dT%H:%M:%S%f%z'
    )
    last_login = serializers.DateTimeField(
        required=False, format='%Y-%m-%dT%H:%M:%S%f%z'
    )
    phones = PhoneSerializer(many=True, required=False)

    class Meta:
        model = User
        exclude = ['id', 'is_active']
        read_only_fields = ['created_at', 'last_login']

    def create(self, validated_data):
        phones = validated_data.pop('phones', [])
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        for phone in phones:
            Phone.objects.create(user=user, **phone)

        return user

    def update(self, instance, validated_data):
        raise serializers.ValidationError('Update not allowed')

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        phones = data.get('phones')

        if not (first_name and last_name and email and password and phones):
            raise serializers.ValidationError(MISSING_FIELD_ERROR)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(EMAIL_ALREADY_REGISTERED_ERROR)

        return data


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=128, required=False)

    def create(self, validated_data):
        email = validated_data.get('email')
        user = User.objects.get(email=email)
        user.update_last_login()

        user_serializer = UserModelSerializer(user)
        response_data = {
            'user': format_data(user_serializer.data),
            'token': get_token_for_user(user)
        }

        return response_data

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')

        if not (email and password):
            raise serializers.ValidationError(MISSING_FIELD_ERROR)

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(INVALID_LOGIN_ERROR)

        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError(INVALID_LOGIN_ERROR)

        return data
