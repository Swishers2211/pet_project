from django.db import models
from django.contrib.auth.models import AbstractUser

CHOICES = (
    ("C", "Клиент"),
    ("M", "Мастер"),
)

class ProjectMaster(models.Model):
    name = models.CharField(max_length=150)


class ProjectClient(models.Model):
    name = models.CharField(max_length=150)


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Почта")
    username = models.CharField(max_length=50, null=True, blank=True, verbose_name="Имя пользователя")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    phone = models.IntegerField(null=True, blank=True, verbose_name="Телефон")
    projects_master = models.OneToOneField(ProjectMaster, verbose_name=("projects_master"), on_delete=models.CASCADE, blank=True, null=True, related_name="projects_master",)
    projects_client = models.OneToOneField(ProjectClient, verbose_name=("projects_client"), on_delete=models.CASCADE, blank=True, null=True, related_name="projects_client",)
    active_role = models.CharField(max_length=300, choices=CHOICES)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Skils(models.Model):
    name = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"


class PortfolioPhoto(models.Model):
    image = models.ImageField(upload_to="portfolio/")

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"


class Portfolio(models.Model):
    title = models.CharField(max_length=250)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    descriptions = models.TextField()
    link = models.URLField("Ссылка на работу", max_length=200)
    photos = models.ManyToManyField(PortfolioPhoto, verbose_name="фотографии")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Портфолио"
        verbose_name_plural = "Портфолио"
