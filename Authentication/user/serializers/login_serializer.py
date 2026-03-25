"""
user/serializers/login_serializer.py
=====================================
Input validation serializer for user login.

Responsibility
--------------
This serializer validates only the presence and format of ``email`` and
``password`` fields.  It deliberately does **NOT** query the database or
generate tokens — that logic belongs in :class:`user.services.AuthService`.

See Also
--------
:meth:`user.services.AuthService.authenticate` — user lookup and token generation.
"""

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Validates login request data (email + password).

    Authentication is handled by :class:`user.services.AuthService`,
    not here.
    """

    email = serializers.EmailField(
        error_messages={
            "required": "Email address is required.",
            "blank": "Email cannot be empty.",
            "invalid": "Please enter a valid email address.",
        },
    )
    password = serializers.CharField(
        write_only=True,
        error_messages={
            "required": "Password is required.",
            "blank": "Password cannot be empty.",
        },
    )
