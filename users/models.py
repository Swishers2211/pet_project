from django.db import models
from django.contrib.auth.models import AbstractUser

class Role:
    roles = (
        ('c', 'Client'),
        ('m', 'Master'),
    )
    role_is_registration = models.CharField(max_length=20, choices=roles)

class User(AbstractUser):
    username = models.CharField(max_length=255, primary_key=True)
    email = models.EmailField(unique=True)
    description = models.TextField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

