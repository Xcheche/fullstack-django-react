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
    http_method_names = ("patch", "get")
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    lookup_field = "public_id"                         # ✅ string field name
    lookup_url_kwarg = "public_id"                     # ✅ kwarg name in URL
    lookup_value_regex = r"[0-9a-f-]{8}-[0-9a-f-]{4}-[0-9a-f-]{4}-[0-9a-f-]{4}-[0-9a-f-]{12}"  # optional but nice

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    # Either REMOVE get_object entirely and let DRF handle it,
    # or make it respect your lookup kwarg:
    def get_object(self):
        public_id = self.kwargs[self.lookup_url_kwarg]   # ✅ no 'pk' hardcode
        obj = User.objects.get_object_by_public_id(public_id)
        self.check_object_permissions(self.request, obj)
        return obj

# ------------------------Register viewset-----------------------#


class RegisterViewSet(ViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)