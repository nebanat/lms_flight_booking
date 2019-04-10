from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    password = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$',
                message='Password must be six alphanumeric character and contain at least one special character'
            )
        ]
    )

    def __str__(self):
        return self.email
