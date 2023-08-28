from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'id', 'email', 'password', 'first_name', 'last_name',
    )
    list_editable = ('password', )
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')


@admin.register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'following')
    list_editable = ('user', 'following')
