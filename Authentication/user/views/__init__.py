"""
user/views/__init__.py
======================
Public API for the views package.

Re-exports all view classes so urls.py can use the simple import::

    from user.views import RegisterView, LoginView, ...
"""

from .auth_views import RegisterView, LoginView, LogoutView
from .profile_views import ProfileView, UserIdentifyView

__all__ = [
    "RegisterView",
    "LoginView",
    "LogoutView",
    "ProfileView",
    "UserIdentifyView",
]
