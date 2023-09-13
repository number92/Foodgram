from django.db import transaction

from djoser.serializers import UserSerializer, UserCreateSerializer

from drf_extra_fields.fields import Base64ImageField


from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import User, Follow
from recipes.models import (
    Tag, Ingredient, Recipe, SumIngredients,
    Favorite, ShoppingList
)
from api.utils import ingredient_list_for_recipe


class SummaryRecipesSerializer(serializers.ModelSerializer):
    """Краткая информация о рецепте"""
    class Meta:

        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeMixin(serializers.ModelSerializer):
    """Дополнительные поля с рецептами для сериализатора подписок"""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        return obj.user.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit', None)
        recipes = obj.user.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = SummaryRecipesSerializer(
            recipes,
            many=True,
            read_only=True
        )
        return serializer.data

    def get_is_subscribed(self, obj):
        user_id = obj.id if isinstance(obj, User) else obj.user.id
        request_user = self.context.get('request').user.id
        queryset = Follow.objects.filter(
            user=user_id,
            following=request_user).exists()
        return queryset


class UserListSerializer(UserSerializer, SubscribeMixin):
    """Список Пользователей, Профиль"""

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed'
        )


class UserWriteSerializer(UserCreateSerializer):
    """ Создание нового пользователя."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'password')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
        }


class SubscriptionSerializer(UserListSerializer, SubscribeMixin):
    """Список подписчиков"""

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed',
            'recipes', 'recipes_count'
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name',
                            'is_subscribed', 'recipes', 'recipes_count'
                            )


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки/отписки от пользователей."""

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны на этого пользователя'
            )
        ]

    def validate(self, data):
        request = self.context.get('request')
        if request.user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.'
            )
        return data

    def to_representation(self, instance):
        return SubscriptionSerializer(
            instance.following, context=self.context).data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор получения тега, списка тегов"""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор получения ингредиента, списка ингредиентов"""
    class Meta:
        model = Ingredient
        fields = '__all__'


class SumIngredientGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации об ингредиентах"""
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = SumIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class SumIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов"""
    id = serializers.IntegerField()

    class Meta:
        model = SumIngredients
        fields = ('id', 'amount')


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка рецептов."""
    tags = TagSerializer(many=True, read_only=True)
    author = UserListSerializer(read_only=True)
    ingredients = SumIngredientGetSerializer(
        many=True, read_only=True, source='recipes'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and Favorite.objects.filter(
                    user=request.user, recipe=obj
                ).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and ShoppingList.objects.filter(
                    user=request.user, recipe_id=obj
                ).exists())


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецептов"""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
    ingredients = SumIngredientsSerializer(many=True, source='recipes')

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients',
                  'tags', 'image',
                  'name', 'text',
                  'cooking_time')
        extra_kwargs = {
            'ingredients': {'required': True, 'allow_blank': False},
            'tags': {'required': True, 'allow_blank': False},
            'name': {'required': True, 'allow_blank': False},
            'text': {'required': True, 'allow_blank': False},
            'image': {'required': True, 'allow_blank': False},
            'cooking_time': {'required': True},
        }

    def validate(self, obj):
        if not obj.get('tags'):
            raise serializers.ValidationError(
                'Нужно указать минимум 1 тег.'
            )
        if not obj.get('recipes'):
            raise serializers.ValidationError(
                'Нужно указать минимум 1 ингредиент.'
            )
        ingredients_list = []
        for ingredient in obj.get('recipes'):
            if ingredient.get('amount') <= 0:
                raise serializers.ValidationError(
                    'Количество не может быть меньше 1'
                )
            ingredients_list.append(ingredient.get('id'))
        if len(set(ingredients_list)) != len(ingredients_list):
            raise serializers.ValidationError(
                'Вы пытаетесь добавить в рецепт два одинаковых ингредиента'
            )
        return obj

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('recipes')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=request.user, **validated_data)
        recipe.tags.set(tags)
        ingredient_list_for_recipe(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipes')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        SumIngredients.objects.filter(recipe=instance).delete()
        super().update(instance, validated_data)
        ingredient_list_for_recipe(ingredients, instance)
        instance.save()
        return instance
