"""
user/services/__init__.py
=========================
Public API for the services package.

The service layer sits between HTTP views and the data layer.
It owns all business logic (user creation, authentication, token management)
keeping views thin and testable::

    from user.services import AuthService
"""

from .auth_service import AuthService

__all__ = ["AuthService"]
