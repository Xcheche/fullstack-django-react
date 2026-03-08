
"""Custom `User` model used by the project.

This model uses email as the `USERNAME_FIELD` and exposes a
stable `public_id` UUID for API lookups. It implements minimal
profile fields and timestamps.
"""

from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from user.manager import UserManager
from django.db import models
from django.http import Http404
from CoreRoot.abstract.models import AbstractModel, AbstractManager


class User(AbstractBaseUser, PermissionsMixin, AbstractModel):
    """Primary user model.

    Fields:
    - `public_id`: UUID used for external lookups (not the DB pk).
    - `email`: unique identifier used for authentication.
    - `username`, `first_name`, `last_name`: profile fields.
    - `is_staff`, `is_active`, `is_superuser`: permission flags.
    - `created`, `updated`, `date_joined`: timestamps.

    The custom manager `UserManager` provides helper methods like
    `get_object_by_public_id` and `create_user`/`create_superuser`.
    """

  
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_superuser = models.BooleanField(default=False)
 

    # Permissions
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    def __str__(self):
        """Human-readable identifier for the user instance."""
        return f"{self.email}"

    @property
    def name(self):
        """Convenience property to return the user's full name."""
        return f"{self.first_name} {self.last_name}"
