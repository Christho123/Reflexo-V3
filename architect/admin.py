from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models.permission import Permission, Role

User = get_user_model()


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'detail', 'guard_name', 'created_at')
    list_filter = ('guard_name', 'created_at')
    search_fields = ('name', 'detail')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'guard_name', 'created_at')
    list_filter = ('guard_name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at') 