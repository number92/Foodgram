from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (
    UserViewSet, TagViewSet,
    IngredientViewSet, RecipeViewSet
    )

router = DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'users', UserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
