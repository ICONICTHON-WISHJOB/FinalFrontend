from rest_framework import serializers
from django.core.validators import RegexValidator
from config.models import CustomUser
from django.contrib.auth.hashers import make_password

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=12, write_only=True)
    phoneNum = serializers.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^01[0-9]{8,9}$', message='Enter a valid phone number')]
    )
    name = serializers.CharField(max_length=10)
    birth = serializers.DateField()

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['email'],
            email=validated_data['email'],
            phoneNum=validated_data['phoneNum'],
            birth=validated_data['birth'],
            first_name=validated_data['name'],
            password=make_password(validated_data['password'])
        )
        user.save()
        return user
