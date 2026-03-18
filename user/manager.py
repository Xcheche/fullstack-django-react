"""Custom manager for the `User` model.

Provides helper methods used across the project for creating users
and resolving user instances by the public UUID. Centralizing this
logic here ensures consistent error handling and normalization.
"""

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from CoreRoot.abstract.models import AbstractManager


class UserManager(BaseUserManager, AbstractManager):
    """Manager with helpers for user creation and lookup.

    Methods:
    - `get_object_by_public_id(public_id)` — return a `User` or raise
      `Http404` for invalid lookups (used by the viewset).
    - `create_user(...)` — create a regular user with normalized email.
    - `create_superuser(...)` — create an admin user with staff/superuser flags.
    """

    def get_object_by_public_id(self, public_id):
        """Return the user matching `public_id` or raise `Http404`.

        Accepts UUID strings or UUID objects and maps common DB/validation
        errors to a single `Http404` response expected by DRF views.
        """
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404

    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with normalized email and hashed password."""
        if username is None:
            raise TypeError("Users must have a username.")
        if email is None:
            raise TypeError("Users must have an email.")
        if password is None:
            raise TypeError("Users must have a password.")
        user = self.model(
            username=username, email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        """Create and return a `User` with superuser (admin) permissions."""
        if password is None:
            raise TypeError("Superusers must have a password.")
        if email is None:
            raise TypeError("Superusers must have an email.")
        if username is None:
            raise TypeError("Superusers must have a username.")
        # create_user expects (username, email, password, ...)
        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
