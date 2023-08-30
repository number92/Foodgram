from django.conf import settings

from djoser.serializers import UserSerializer, UserCreateSerializer

from rest_framework import serializers

from users.models import User, Follow


class UserListSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed'
            )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous or (user == obj):
            return False
        return Follow.objects.filter(
                user=user,
                following=obj).exists()


class UserCreateSerializer(UserCreateSerializer):
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


class SubscriptionSerializer(UserListSerializer):
    """Список подписчиков"""
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed',
            # 'recipe', 'recipes_count'
            )
        read_only_fields = ("__all__",)
