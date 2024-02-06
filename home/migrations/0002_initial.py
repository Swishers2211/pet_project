# Generated by Django 4.2.1 on 2024-02-02 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='respond',
            name='master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Мастер'),
        ),
        migrations.AddField(
            model_name='respond',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.project', verbose_name='Проект'),
        ),
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='project',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='project',
            name='main_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.main_category', verbose_name='Главная категория'),
        ),
        migrations.AddField(
            model_name='project',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.sub_category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='category',
            name='main_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.main_category', verbose_name='Категория'),
        ),
    ]
