"""
user/serializers/register_serializer.py
========================================
Input validation serializer for user registration.

Responsibility
--------------
This serializer is ONLY responsible for validating the shape and rules of
incoming registration data.  No business logic lives here.

Validation rules enforced
--------------------------
- ``username``  : required, unique (case-insensitive)
- ``email``     : required, valid format, unique (case-insensitive)
- ``password``  : required, min 6 chars, not entirely numeric
- ``first_name``: optional
- ``last_name`` : optional

See Also
--------
:class:`user.services.AuthService.create_user` — actual user creation logic.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """
    Validates registration request data.

    Does NOT create a user — that is delegated to
    :meth:`user.services.AuthService.create_user`.
    """

    username = serializers.CharField(
        max_length=150,
        error_messages={
            "required": "Username is required.",
            "blank": "Username cannot be empty.",
            "max_length": "Username cannot exceed 150 characters.",
        },
    )
    email = serializers.EmailField(
        error_messages={
            "required": "Email address is required.",
            "blank": "Email cannot be empty.",
            "invalid": "Please enter a valid email address.",
        },
    )
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        error_messages={
            "required": "Password is required.",
            "blank": "Password cannot be empty.",
            "min_length": "Password must be at least 6 characters.",
        },
    )
    first_name = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )
    last_name = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )

    # ── Field-level validators ──────────────────────────────────────────────

    def validate_email(self, value: str) -> str:
        """Normalise email to lowercase and enforce uniqueness."""
        email = value.lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )
        return email

    def validate_username(self, value: str) -> str:
        """Enforce case-insensitive username uniqueness."""
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "This username is already taken. Please choose another."
            )
        return value

    def validate_password(self, value: str) -> str:
        """Reject passwords that are entirely numeric (security best practice)."""
        if value.isdigit():
            raise serializers.ValidationError(
                "Password cannot consist of numbers only."
            )
        return value
