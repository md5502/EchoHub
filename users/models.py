from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from config.settings import AUTH_USER_MODEL

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    last_seen = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, related_name="Profile", on_delete=models.CASCADE)
    profile_image = models.ImageField(_("profile image"), upload_to="usres/profiles", blank=True,null=True)
    display_name = models.CharField(_("display name"), max_length=50, blank=True,null=True)
    bio = models.TextField(_("biography"), blank=True,null=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.user.username
