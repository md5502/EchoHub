from dj_rest_auth import serializers as dj_serializers
from rest_framework import serializers

from users.models import CustomUser, UserProfile


class LoginSerializer(dj_serializers.LoginSerializer):
    email = None


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["display_name", "bio", "profile_image", "created_at", "updated_at"]


class UserDetailsSerializer(dj_serializers.UserDetailsSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "last_seen", "is_active", "profile"]

    def get_profile(self, obj):
        try:
            profile = UserProfile.objects.get(user=obj)
            return UserProfileSerializer(profile).data
        except UserProfile.DoesNotExist:
            return None
