from django.contrib import admin
from . import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'image',
                    'text', 'cooking_time')


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ("name",)

@admin.register(models.SumIngredients)
class SumIngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount',)
    list_editable = ('amount',)
    empty_value_display = '-------'


@admin.register(models.ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe_id')
    list_editable = ('user', 'recipe_id')
    empty_value_display = '-------'
