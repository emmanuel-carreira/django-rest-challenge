from django.core.validators import EmailValidator
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, required=False)
    last_name = serializers.CharField(max_length=50, required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=255, write_only=True)
    created_at = serializers.DateTimeField(required=False)
    last_login = serializers.DateTimeField(required=False)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['created_at', 'last_login']

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

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
