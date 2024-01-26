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

class Client(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    
    def __str__(self):
        return self.client.user.email

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Master(models.Model):
    master = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    
    def __str__(self):
        return self.master.user.email

    class Meta:
        verbose_name = 'Фрилансер'
        verbose_name_plural = 'Фрилансеры'
