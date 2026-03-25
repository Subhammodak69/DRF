"""
user/views/profile_views.py
============================
HTTP controllers for user profile/identity operations.

All endpoints here require JWT authentication.

Endpoints
---------
- ``GET /api/auth/profile/`` → :class:`ProfileView`
- ``GET /api/auth/user/``    → :class:`UserIdentifyView`
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.services import AuthService


class ProfileView(APIView):
    """
    GET /api/auth/profile/
    -----------------------
    Returns the authenticated user's profile.

    **Auth required**: Yes (Bearer token)

    Success response (200)::

        {
            "id":         1,
            "username":   "johndoe",
            "email":      "john@example.com",
            "first_name": "John",
            "last_name":  "Doe"
        }

    Error response (401)::

        { "error": "Authentication credentials were not provided." }
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )


class UserIdentifyView(APIView):
    """
    GET /api/auth/user/
    --------------------
    Returns extended user information including account status and join date.

    Used by the frontend ``AuthContext`` on app load to hydrate the user state
    from a stored access token without requiring a fresh login.

    **Auth required**: Yes (Bearer token)

    Success response (200)::

        {
            "id":          1,
            "username":    "johndoe",
            "email":       "john@example.com",
            "first_name":  "John",
            "last_name":   "Doe",
            "is_active":   true,
            "date_joined": "2025-01-15T08:30:00Z"
        }

    Error response (401)::

        { "error": "Authentication credentials were not provided." }
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Delegate serialisation to the service layer
        return Response(AuthService.get_user_data(request.user))
