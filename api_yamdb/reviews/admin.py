from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomAdmin(UserAdmin):

    model = User
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bio',)}),
        ('Permissions', {'fields': ('role', 'is_moderator')})
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        ('Permissions', {'fields': ('role', 'is_moderator')})
    )

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    ]
