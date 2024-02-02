from django.db import models

from users.models import User

'''Главная категория Main_Category'''
class Main_Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    published = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Главная категория'
        verbose_name_plural = 'Главные категории'

'''Подкатегория Category гланой категории Main_Category'''
class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE, verbose_name='Категория')
    published = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
'''Подккатегория Sub_Category подкатегории Category'''
class Sub_Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    published = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

'''Клиент может выставить свой проект'''
class Project(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    image = models.ImageField(upload_to='project_image', verbose_name='Фото проекта', null=True, blank=True)
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE, verbose_name='Главная категория')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=7, decimal_places=0, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):  
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

'''Отклики на проект (у мастера и клиента)'''
class Respond(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    master = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Мастер')
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.project.name

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
