from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("accountant", "Accountant"),
        ("front_desk", "Front Desk"),
    )

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_full_name() or self.username