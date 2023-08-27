from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=settings.NAME_LENGTH,
        verbose_name='Имя',
        unique=True,
    )
    color = models.CharField(
        max_length=settings.COLOR_LENGTH,
        verbose_name='Код цвета',
        unique=True,
    )
    slug = models.SlugField(
        max_length=settings.NAME_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=settings.NAME_LENGTH,
        verbose_name='Название',
        unique=True,
    )
    measurement_unit = models.CharField(
        max_length=settings.UNIT_LENGTH,
        verbose_name='Единица измерения',
        blank=False,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='user',
        verbose_name='Автор',
    )
    tags = models.ManyToManyField(
        Tag,
        null=True,
        related_name='recipes',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        null=True,
        through='SumIngredients',
        through_fields=('recipe_id', 'ingredient_id'),
        verbose_name='Ингредиенты'
    )
    name = models.CharField(
        max_length=settings.NAME_LENGTH,
        verbose_name='Название',
        unique=True,
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
        editable=False,
    )
    image = models.ImageField(
        verbose_name="Изображение блюда",
        upload_to="/media/recipe_images/",
    )
    text = models.TextField(
        verbose_name="Описание блюда",
        max_length=settings.TEXT_LENGHT
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        default=0
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class SumIngredients(models.Model):
    recipe_id = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт'
    )
    ingredient_id = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        'Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient'
            )
        ]

    def __str__(self):
        amount_unit = f'{self.amount} {self.ingredient_id.measurement_unit}'
        return (
            f'{self.recipe_id.name}: '
            f'{self.ingredient_id.name} - {amount_unit}'
            )

class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_recipe_list',
        verbose_name='Список рецептов пользователя'
    )
    recipe_id = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='list_of_recipes',
        verbose_name='Список рецептов'
    )

    class Meta:
        verbose_name = 'Список рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_list'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe_id.name}'