from django.contrib.auth.models import AbstractUser
from django.db import models

from rest_framework import generics
from .serializers import UserSignupSerializer

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class UserSignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSignupSerializer