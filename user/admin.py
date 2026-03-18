"""Admin registration for `user` app models.

Keep admin registration minimal — interns can use Django admin to
inspect `User` records during development.
"""

from django.contrib import admin
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for the `User` model.

    For now we register the model with default behaviour. Add search,
    list_display etc. later as needed for admin convenience.
    """

    pass
