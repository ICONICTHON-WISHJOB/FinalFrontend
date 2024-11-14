from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser

class SignupSerializer(serializers.ModelSerializer):
    experience = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField(), required=False),
        required=False,
        allow_empty=True
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 'password', 'phoneNum', 'full_name', 'birth', 'age', 'school', 'department',
            'admission_date', 'graduation_date', 'experience', 'self_introduction', 'companies_of_interest'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        experience = validated_data.pop('experience', [])
        user = super().create(validated_data)
        if experience:
            user.experience = experience
            user.save()
        return user
