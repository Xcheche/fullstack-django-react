from rest_framework import serializers

from django.contrib.auth import get_user_model
from user.models import User
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()


#---------------------Custom user serializer---------------------#
class UserSerializer(serializers.ModelSerializer):
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
#---------------------Custom user serializer ends---------------------#



#---------------------User registration serializer---------------------#
class RegisterSerializer(serializers.ModelSerializer):
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

    # Creating user with custom manager create_user method
    def create(self, validated_data):
        password = validated_data.pop("password")
        # uses custom manager → handles email normalization, etc.
        user = User.objects.create_user(password=password, **validated_data)
        return user



#------------------------------Login Serializer---------------------------------------
class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["user"] = UserSerializer(self.user).data
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data