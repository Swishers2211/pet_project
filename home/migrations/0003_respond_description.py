# Generated by Django 4.2.1 on 2024-02-05 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='respond',
            name='description',
            field=models.TextField(default=1, verbose_name='Опишите себя и свой опыт'),
            preserve_default=False,
        ),
    ]
