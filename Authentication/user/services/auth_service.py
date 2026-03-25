"""
user/services/auth_service.py
==============================
Business logic layer for all authentication operations.

Design Principles
-----------------
- Views are thin HTTP adapters — they delegate ALL logic here.
- This class has **no knowledge of HTTP** (no Request/Response objects).
- Each method raises ``serializers.ValidationError`` on expected failures
  so the global exception handler can normalise them to ``{"error": "..."}``.
- All unexpected exceptions propagate up as 500s — never swallow them silently.

Usage::

    from user.services import AuthService

    # In a view:
    tokens = AuthService.authenticate(email, password)
    user   = AuthService.create_user(validated_data)
    AuthService.logout(refresh_token)
"""

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


class AuthService:
    """
    Stateless service class for authentication business logic.

    All methods are static — no instance state is needed.
    """

    # ── Registration ────────────────────────────────────────────────────────

    @staticmethod
    def create_user(validated_data: dict) -> User:
        """
        Create and persist a new user account.

        Parameters
        ----------
        validated_data : dict
            Pre-validated data from :class:`user.serializers.RegisterSerializer`.
            Expected keys: ``username``, ``email``, ``password``,
            ``first_name`` (optional), ``last_name`` (optional).

        Returns
        -------
        User
            The newly created (and saved) User instance.

        Raises
        ------
        serializers.ValidationError
            If a database-level constraint is violated after serializer checks.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user

    # ── Authentication ───────────────────────────────────────────────────────

    @staticmethod
    def authenticate(email: str, password: str) -> dict:
        """
        Verify credentials and generate a JWT access/refresh token pair.

        Parameters
        ----------
        email : str
            The user's email address (case-insensitive lookup).
        password : str
            The plain-text password to verify against the stored hash.

        Returns
        -------
        dict
            ``{ "access": str, "refresh": str, "email": str }``

        Raises
        ------
        serializers.ValidationError
            - If no account exists for the given email.
            - If the password does not match.
            - If the account is inactive/disabled.
        """
        # Case-insensitive email lookup
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No account found with this email address."
            )

        # Password verification
        if not check_password(password, user.password):
            raise serializers.ValidationError(
                "Incorrect password. Please try again."
            )

        # Active account check
        if not user.is_active:
            raise serializers.ValidationError(
                "Your account has been disabled. Please contact support."
            )

        # Generate JWT tokens via SimpleJWT
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "email": user.email,
        }

    # ── Logout / Token Blacklisting ──────────────────────────────────────────

    @staticmethod
    def logout(refresh_token: str) -> None:
        """
        Blacklist a refresh token to invalidate the user's session.

        Silently succeeds if the token is already expired or invalid
        (the client is already effectively logged out in those cases).

        Parameters
        ----------
        refresh_token : str
            The refresh token string from the client's request body.

        Returns
        -------
        None

        Raises
        ------
        Nothing — expired/invalid tokens are treated as already-logged-out.
        """
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            # Token already expired or invalid — user is already logged out.
            pass

    # ── User Info ────────────────────────────────────────────────────────────

    @staticmethod
    def get_user_data(user: User) -> dict:
        """
        Serialise a User instance into a safe, JSON-ready dict.

        Parameters
        ----------
        user : User
            An authenticated User instance from ``request.user``.

        Returns
        -------
        dict
            Safe user fields — never includes password or sensitive data.
        """
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "date_joined": user.date_joined,
        }
