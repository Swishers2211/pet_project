from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Почта')
    username = models.CharField(max_length=50, null=True, blank=True, verbose_name='Имя пользователя')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    phone = models.IntegerField(null=True, blank=True, verbose_name='Телефон')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
