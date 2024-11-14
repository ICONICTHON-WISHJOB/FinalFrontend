from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phoneNum = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(regex=r'^01[0-9]{8,9}$', message='Enter a valid phone number')]
    )
    birth = models.DateField()

    full_name = models.CharField(max_length=255, default="")
    age = models.PositiveIntegerField(null=True, blank=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    graduation_date = models.DateField(null=True, blank=True)

    experience = models.JSONField(null=True,blank=True)

    self_introduction = models.TextField(null=True, blank=True)
    companies_of_interest = models.TextField(null=True, blank=True)

    REQUIRED_FIELDS = ['phoneNum', 'birth', 'full_name']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.full_name  # Set username to full_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Company(models.Model):
    name = models.CharField(max_length=255)
    company_id = models.EmailField(max_length=50, unique=True)  # Unique ID for each company
    promotional_content = models.TextField()
    applicants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='interested_companies', blank=True)

    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.company_id})"

class Booth(models.Model):
    booth_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='booths')
    day = models.CharField(default=0)
    floor = models.CharField(default=0)
    boothNum = models.CharField(max_length=10, unique=True, null=True)
    boothCate = models.CharField(max_length=100, null=True)
    boothName = models.CharField(max_length=255, null=True)

    queue = models.ManyToManyField(
        CustomUser,
        related_name='waiting_booths',
        blank=True,
        through='BoothQueue'
    )

    past_participants = models.ManyToManyField(
        CustomUser,
        related_name='participated_booths',
        blank=True
    )

    def __str__(self):
        return f"Booth {self.booth_id} - {self.company.name} on {self.day}"

class BoothQueue(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()  # Position in the queue

    class Meta:
        unique_together = ['booth', 'user']
        ordering = ['position']  # Orders queue by position

    def __str__(self):
        return f"User {self.user.full_name} in queue for Booth {self.booth.booth_id} at position {self.position}"
