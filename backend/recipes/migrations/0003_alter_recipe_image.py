# Generated by Django 3.2 on 2023-09-13 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipe/images/', verbose_name='Изображение блюда'),
        ),
    ]
