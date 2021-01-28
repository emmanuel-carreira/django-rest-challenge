from django.core.validators import EmailValidator
from rest_framework import serializers

from .models import Profile, Phone


class PhoneSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(max_value=2147483647, required=False)
    area_code = serializers.IntegerField(max_value=32767, required=False)
    country_code = serializers.CharField(max_length=4, required=False)

    class Meta:
        model = Phone
        exclude = ['profile']

    def update(self, instance, validated_data):
        raise serializers.ValidationError('Update not allowed')

    def validate(self, data):
        number = data.get('number')
        area_code = data.get('area_code')
        country_code = data.get('country_code')

        if not (number and area_code and country_code):
            raise serializers.ValidationError('Missing fields')

        return data


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, required=False)
    last_name = serializers.CharField(max_length=50, required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=255, write_only=True)
    created_at = serializers.DateTimeField(required=False)
    last_login = serializers.DateTimeField(required=False)
    phones = PhoneSerializer(many=True)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['created_at', 'last_login']

    def create(self, validated_data):
        phones = validated_data.pop('phones', [])
        profile = Profile.objects.create(**validated_data)

        for phone in phones:
            Phone.objects.create(profile=profile, **phone)

        return profile

    def update(self, instance, validated_data):
        raise serializers.ValidationError('Update not allowed')

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        if not (first_name and last_name and email and password):
            raise serializers.ValidationError('Missing fields')

        if Profile.objects.filter(email=email).exists():
            raise serializers.ValidationError('E-mail already exists')

        return data
