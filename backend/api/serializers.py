from django.conf import settings

from djoser.serializers import UserSerializer, UserCreateSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import User, Follow


class SubscribeMixin(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user_id = obj.id if isinstance(obj, User) else obj.user.id
        request_user = self.context.get('request').user.id
        queryset = Follow.objects.filter(
            user=user_id,
            following=request_user).exists()
        return queryset


class UserListSerializer(UserSerializer, SubscribeMixin):
    """Список Пользователей, Профиль"""
    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed'
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


class SubscriptionSerializer(UserListSerializer, SubscribeMixin):
    """Список подписчиков"""

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed',
            # 'recipe', 'recipes_count'
            )
        read_only_fields = ('email', 'username', 'first_name',
                            'last_name', 'is_subscribed',)


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
