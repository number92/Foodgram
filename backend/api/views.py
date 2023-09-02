from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from users.models import User, Follow
from api.pagination import LimitPagination
from api.serializers import (SubscriptionSerializer, SubscribeSerializer)


class UserViewSet(DjoserViewSet):
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
        print(request.user.id)
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author,
                context={'request': request,
                         'user': request.user.id,
                      'following': author.id
                         },
                data={'user': request.user.id,
                      'following': author.id}
                )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=request.user, following=author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Follow.objects.filter(
                user=request.user, following=author).exists():
                return Response(
                    {'errors': 'Вы не подписаны на этого пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            get_object_or_404(Follow, user=request.user,
                              following=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
