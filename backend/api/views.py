from django.db.models import Sum
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.response import Response
from rest_framework import viewsets, status, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from api.permissions import CurrentUserOrAdminOrReadOnly
from api.pagination import LimitPagination
from api.filters import RecipeFilter
from api.serializers import (
    SubscriptionSerializer, SubscribeSerializer,
    TagSerializer, IngredientSerializer,
    RecipeGetSerializer, RecipeCreateSerializer,
    SummaryRecipesSerializer
    )
from users.models import User, Follow
from recipes.models import (
    Tag, Ingredient, Recipe, Favorite,
    ShoppingList, SumIngredients
)


class UserViewSet(DjoserViewSet):
    """
    Регистрация, авторизация, смена пароля, список пользователей,
    профиль пользователя, свой профиль /me,
    список подписок, подписаться, отписаться
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitPagination

    @action(detail=False,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        serializer = SubscriptionSerializer(
            self.paginate_queryset(queryset),
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = SubscribeSerializer(
                context={'request': request},
                data={'user': request.user.id,
                      'following': author.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Follow.objects.filter(
                user=request.user,
                following=author
            ).exists():
                return Response(
                    {'errors': 'Вы не подписаны на этого пользователя'},
                    status=status.HTTP_400_BAD_REQUEST)
            get_object_or_404(Follow, user=request.user,
                              following=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации о тегах."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации об ингредиентах."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (CurrentUserOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitPagination
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeCreateSerializer

    @action(detail=True,
            permission_classes=(IsAuthenticated,),
            queryset=Favorite.objects.all(),
            pagination_class=None,
            methods=['POST', 'DELETE']
            )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = SummaryRecipesSerializer(
                recipe, data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            if not Favorite.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                Favorite.objects.create(user=request.user, recipe=recipe)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже добавлен в избранное.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'DELETE':
            get_object_or_404(
                Favorite, user=request.user, recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,),
            pagination_class=None
            )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = SummaryRecipesSerializer(
                recipe, data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            if not ShoppingList.objects.filter(
                    user=request.user, recipe_id=recipe).exists():
                ShoppingList.objects.create(
                    user=request.user,
                    recipe_id=recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {'errors': 'Рецепт уже в списке покупок.'},
                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            get_object_or_404(
                ShoppingList, user=request.user,
                recipe_id=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
            detail=False,
            permission_classes=(IsAuthenticated,),
            methods=['GET']
            )
    def download_shopping_cart(self, request):
        ingredients = (
            SumIngredients.objects.filter(
                recipe__recipe_list__user=request.user
                ).values('ingredient').annotate(
                    total_amount=Sum('amount')
                    ).values_list(
                        'ingredient__name',
                        'total_amount',
                        'ingredient__measurement_unit'
                    )
            )
        file_list = []
        [file_list.append(
            '{} - {} {}.'.format(*ingredient)) for ingredient in ingredients]
        response = HttpResponse(
            'Cписок покупок:\n' + '\n'.join(file_list),
            content_type='text/plain'
            )
        response['Content-Disposition'] = (
            f'attachment; filename={settings.FILE_NAME}'
            )
        return response
