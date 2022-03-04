from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'trainer']


admin.site.register(User, UserAdmin)
