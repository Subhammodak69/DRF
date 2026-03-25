"""
user/models/user_model.py
=========================
Documentation module for the User model used throughout this project.

This application uses Django's built-in ``AbstractUser`` model (accessed via
``django.contrib.auth.get_user_model()``) rather than a custom model.

Fields available on the User model
------------------------------------
- ``id``           : int  — auto-incrementing primary key
- ``username``     : str  — unique username (max 150 chars)
- ``email``        : str  — email address (not unique by default, enforced in serializer)
- ``first_name``   : str  — optional given name
- ``last_name``    : str  — optional family name
- ``password``     : str  — hashed password (never store plain text)
- ``is_active``    : bool — False = account disabled
- ``is_staff``     : bool — True = can access Django admin
- ``is_superuser`` : bool — True = all permissions
- ``date_joined``  : datetime — account creation timestamp
- ``last_login``   : datetime — last successful login

If a custom User model is needed in the future, create it here by extending
``AbstractUser`` or ``AbstractBaseUser``, then point ``AUTH_USER_MODEL`` in
settings.py to ``'user.CustomUser'``.

Example (future custom model)::

    from django.contrib.auth.models import AbstractUser
    from django.db import models

    class CustomUser(AbstractUser):
        phone_number = models.CharField(max_length=20, blank=True)
        avatar_url   = models.URLField(blank=True)

        class Meta:
            verbose_name = 'User'
            verbose_name_plural = 'Users'
"""

from django.contrib.auth import get_user_model

# Public alias — prefer importing from user.models directly.
User = get_user_model()
