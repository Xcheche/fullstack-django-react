"""API viewsets for the `user` app.

This module exposes DRF viewsets used for user management:
- `UserViewSet` - read/patch access to user records (lookup by `public_id`).
- `RegisterViewSet` - registers a new user and returns JWT tokens.
- `LoginViewSet` - exchanges credentials for access/refresh tokens.
- `RefreshViewSet` - handles refresh token exchange.

Docstrings and comments inside each class explain inputs, outputs
and important implementation notes so new developers (or interns)
can quickly understand how authentication flows work.
"""

import uuid
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from user.serializers import UserSerializer
from user.models import User
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers import RegisterSerializer
from user.serializers import LoginSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView


# ----------------Custom User viewset------------------
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for retrieving and updating users.

    Only `GET` and `PATCH` HTTP methods are allowed. Lookup is performed
    by `public_id` (a UUID) instead of the numeric primary key so the API
    remains stable even if database primary keys are exposed.

    - `get_queryset`: limits visible users for non-superusers.
    - `get_object`: resolves `public_id` to the `User` instance using
      the custom manager helper `get_object_by_public_id` which raises
      `Http404` for invalid values.
    """

    http_method_names = ("patch", "get")
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    lookup_field = "public_id"
    lookup_url_kwarg = "public_id"
    lookup_value_regex = r"[0-9a-f-]{8}-[0-9a-f-]{4}-[0-9a-f-]{4}-[0-9a-f-]{4}-[0-9a-f-]{12}"

    def get_queryset(self):
        """Return a QuerySet of users this requestor can see.

        Superusers see all users; regular users cannot list superusers.
        This keeps the API minimal while hiding admin accounts.
        """
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        """Resolve and return a `User` instance using `public_id`.

        We rely on the custom manager `get_object_by_public_id` which
        centralizes the lookup behaviour and raises `Http404` on
        invalid input — useful for consistent error responses.
        """
        #like details view, we need to override get_object to use the custom manager's lookup method
        public_id = self.kwargs[self.lookup_url_kwarg]
        obj = User.objects.get_object_by_public_id(public_id)
        self.check_object_permissions(self.request, obj)
        return obj

# ------------------------Register viewset-----------------------#


class RegisterViewSet(ViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]
    """Endpoint to create a new user and return JWT tokens.

    Expects data matching `RegisterSerializer`. On success returns
    `user` representation plus `refresh` and `access` tokens.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(
            {
                "user": serializer.data,
                "refresh": res["refresh"],
                "token": res["access"],
            },
            status=status.HTTP_201_CREATED,
        )


#-------------------------------Login Viewset---------------
class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]
    """Authenticate a user and return JWT tokens and user data.

    This view delegates to `LoginSerializer` (which extends
    `TokenObtainPairSerializer`) to validate credentials and
    construct the token response.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


#--------------------------------Refresh Token Viewset----------------#
class RefreshViewSet(ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    """Refresh access tokens using a valid refresh token.

    This class mixes `ViewSet` with SimpleJWT's `TokenRefreshView` so
    it can be registered on a router while preserving SimpleJWT's
    serializer and validation behaviour.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)