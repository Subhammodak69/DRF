"""
user/views/auth_views.py
========================
HTTP controllers for authentication operations.

Controller Responsibilities (thin layer)
-----------------------------------------
1. Validate the incoming request data via a serializer.
2. Delegate business logic to :class:`user.services.AuthService`.
3. Return a structured HTTP response.

Controllers here must NOT contain business logic.

Endpoints
---------
- ``POST /api/auth/register/`` → :class:`RegisterView`
- ``POST /api/auth/login/``    → :class:`LoginView`
- ``POST /api/auth/logout/``   → :class:`LogoutView`
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import RegisterSerializer, LoginSerializer
from user.services import AuthService


class RegisterView(APIView):
    """
    POST /api/auth/register/
    ------------------------
    Creates a new user account.

    **Auth required**: No (public endpoint)

    Request body::

        {
            "username":   "johndoe",
            "email":      "john@example.com",
            "password":   "secret123",
            "first_name": "John",   // optional
            "last_name":  "Doe"     // optional
        }

    Success response (201)::

        {
            "message": "Account created successfully. Please sign in.",
            "user": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe"
            }
        }

    Error response (400)::

        { "error": "<human-readable message>" }
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        # raise_exception=True → global handler formats the error
        serializer.is_valid(raise_exception=True)

        user = AuthService.create_user(serializer.validated_data)

        return Response(
            {
                "message": "Account created successfully. Please sign in.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    POST /api/auth/login/
    ----------------------
    Authenticates the user and returns a JWT access + refresh token pair.

    **Auth required**: No (public endpoint)

    Request body::

        {
            "email":    "john@example.com",
            "password": "secret123"
        }

    Success response (200)::

        {
            "access":  "<jwt-access-token>",
            "refresh": "<jwt-refresh-token>",
            "email":   "john@example.com"
        }

    Error response (400)::

        { "error": "<human-readable message>" }
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = AuthService.authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response(tokens, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    -----------------------
    Blacklists the provided refresh token to invalidate the session.

    **Auth required**: Yes (Bearer token)

    Request body::

        { "refresh": "<jwt-refresh-token>" }

    Success response (200)::

        { "message": "Signed out successfully." }

    Error response (400)::

        { "error": "Refresh token is required to sign out." }

    Notes
    -----
    If the token is already expired or invalid, the logout still succeeds
    (the client is already effectively logged out).
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required to sign out."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Service handles TokenError silently
        AuthService.logout(refresh_token)

        return Response(
            {"message": "Signed out successfully."},
            status=status.HTTP_200_OK,
        )
