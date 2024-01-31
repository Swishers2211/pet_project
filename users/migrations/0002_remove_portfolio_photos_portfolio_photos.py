# Generated by Django 4.2.1 on 2024-01-31 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='photos',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='photos',
            field=models.ManyToManyField(to='users.portfoliophoto', verbose_name='фотографии'),
        ),
    ]
