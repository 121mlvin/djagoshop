from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)

    def __str__(self):
        return f"Name: {self.username}, wallet: {self.wallet}"
