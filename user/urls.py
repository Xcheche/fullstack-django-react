"""URL routing for the `user` app.

This module registers viewsets on a `SimpleRouter` to expose a small
REST API for user operations. Note the JWT refresh endpoint from
SimpleJWT is wired as a separate view because the router routes are
used for the viewset endpoints.
"""

from django.urls import path, include
from rest_framework import routers
from user.viewsets import LoginViewSet, UserViewSet, RegisterViewSet
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView


router = routers.SimpleRouter()
router.register(r"", UserViewSet, basename="user")
router.register(r"register", RegisterViewSet, basename="register")
router.register(r"login", LoginViewSet, basename="login")


urlpatterns = [
    path("", include(router.urls)),
    # JWT token refresh endpoint must be setup separately
    path("token/refresh/", SimpleJWTTokenRefreshView.as_view(), name="token_refresh"),
]
