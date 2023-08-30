from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    # path(r'', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
]
