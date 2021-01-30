from django.core.validators import EmailValidator
from rest_framework import serializers

from .models import User, Phone


class PhoneSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(max_value=2147483647, required=False)
    area_code = serializers.IntegerField(max_value=32767, required=False)
    country_code = serializers.CharField(max_length=4, required=False)

    class Meta:
        model = Phone
        exclude = ['user']

    def update(self, instance, validated_data):
        raise serializers.ValidationError('Update not allowed')

    def validate(self, data):
        number = data.get('number')
        area_code = data.get('area_code')
        country_code = data.get('country_code')

        if not (number and area_code and country_code):
            raise serializers.ValidationError('Missing fields')

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
    created_at = serializers.DateTimeField(required=False)
    last_login = serializers.DateTimeField(required=False)
    phones = PhoneSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = '__all__'
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
            raise serializers.ValidationError('Missing fields')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('E-mail already exists')

        return data
