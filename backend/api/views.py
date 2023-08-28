from django.shortcuts import render
from users.models import User, Follow

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAdmin,)
    # # filter_backends = (filters.SearchFilter,)
    # # # search_fields = ('username',)
    # # # lookup_field = 'username'