from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=settings.NAME_LENGTH,
        verbose_name='Имя',
        unique=True,
        blank=False,
    )
    color = models.CharField(
        max_length=settings.COLOR_LENGTH,
        verbose_name='Код цвета',
        unique=True,
        blank=False,
    )
    slug = models.SlugField(
        max_length=settings.NAME_LENGTH,
        unique=True,
        blank=False,
    )
    
class Ingredient(models.Model):
    name = models.CharField(
        max_length=settings.NAME_LENGTH,
        verbose_name='Название',
        unique=True,
        blank=False,
    )
    measurment_unit = models.CharField(
        max_length=settings.NAME_LENGTH,
        verbose_name='Единица измерения',
        unique=True,
        blank=False,
    )