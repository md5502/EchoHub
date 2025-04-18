from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("get_username", "display_name", "short_bio", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")

    def get_username(self, obj):
        return obj.user.username

    def short_bio(self, obj):
        return obj.bio[:30] + "..."


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "last_seen", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("email", "last_seen")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("username", "email", "password1", "password2", "is_staff", "is_active")},
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
