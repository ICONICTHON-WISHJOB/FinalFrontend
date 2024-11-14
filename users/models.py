from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phoneNum = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(regex=r'^01[0-9]{8,9}$', message='Enter a valid phone number')]
    )
    birth = models.DateField()

    REQUIRED_FIELDS = ['phoneNum', 'birth', 'first_name']

    def __str__(self):
        return self.username
