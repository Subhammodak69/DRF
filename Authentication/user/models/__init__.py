"""
user/models/__init__.py
=======================
Re-exports the active User model so any module can do:

    from user.models import User

instead of calling get_user_model() everywhere.
"""

from django.contrib.auth import get_user_model

User = get_user_model()

__all__ = ["User"]
