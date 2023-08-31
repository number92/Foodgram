from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from users.models import User, Follow
from api.pagination import LimitPagination
from api.serializers import (UserListSerializer, 
                             UserCreateSerializer,
                             SubscriptionSerializer)


class UserViewSet(DjoserViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitPagination

    @action(detail=False,
            permission_classes=(IsAuthenticated,))
    def subcriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        serializer = SubscriptionSerializer(self.paginate_queryset(queryset),
                                            many=True,
                                            context={'request': request})
        return self.get_paginated_response(serializer.data)
