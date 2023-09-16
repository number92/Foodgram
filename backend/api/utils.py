from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, SumIngredients


def ingredient_list_for_recipe(ingredients, recipe):
    '''Создание списка ингредиентов для рецепта.'''
    ingredient_list = []
    for ingredient in ingredients:
        current_ingredient = get_object_or_404(
            Ingredient, id=ingredient.get('id'))
        amount = ingredient.get('amount')
        ingredient_list.append(
            SumIngredients(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=amount
            )
        )
    SumIngredients.objects.bulk_create(ingredient_list)
