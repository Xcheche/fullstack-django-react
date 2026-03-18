"""DRF serializers for the `user` app.

This module exposes:
- `UserSerializer` — representation used by the API for user objects.
- `RegisterSerializer` — handles user creation and password write-only
  behaviour.
- `LoginSerializer` — extends SimpleJWT's `TokenObtainPairSerializer`
  to include serialized user data plus tokens in the response.
"""

from rest_framework import serializers

from django.contrib.auth import get_user_model
from user.models import User
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from CoreRoot.abstract.serializers import AbstractSerializer

User = get_user_model()


class UserSerializer(AbstractSerializer):
    """Serializer for returning `User` objects in API responses.

    - `id` exposes the internal `public_id` UUID as a read-only value.
    - `created` and `updated` are read-only timestamps.
    """

    id = serializers.UUIDField(source="public_id", read_only=True, format="hex")
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            # "bio",
            # "avatar",
            "email",
            "is_active",
            "created",
            "updated",
        ]
        read_only_field = ["is_active"]


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer used when creating new users via the API.

    The `password` field is write-only and must meet length restrictions.
    The `create` method delegates to the custom manager's
    `create_user` method so normalization and password hashing are
    handled consistently.
    """

    password = serializers.CharField(write_only=True, min_length=8, max_length=128)

    class Meta:
        model = User
        fields = (
            "public_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )
        read_only_fields = ("public_id",)

    def create(self, validated_data):
        """Create a new user using the model manager.

        We pop the password to avoid storing it directly and call
        `User.objects.create_user(...)` which applies normalization and
        sets the hashed password.
        """
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    """Extend SimpleJWT serializer to include serialized user data.

    The `validate` method returns a payload that includes the user
    representation plus `refresh` and `access` tokens. It also updates
    the last login timestamp if configured in SimpleJWT settings.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["user"] = UserSerializer(self.user).data
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data
