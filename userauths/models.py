from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=150, verbose_name="Nom d'utilisateur")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    bio = models.CharField(max_length=1000, verbose_name="Biographie")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.username}"
