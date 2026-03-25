from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer


class RegisterView(APIView):
    """
    POST /api/auth/register/
    Creates a new user account.
    Success  → 201 { message, user: { id, username, email, first_name, last_name } }
    Failure  → 400 { error: "<user-facing message>" }    (via global handler)
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)       # global handler formats this
        user = serializer.save()
        return Response({
            'message': 'Account created successfully. Please sign in.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    POST /api/auth/login/
    Authenticates with email + password, returns JWT pair.
    Success  → 200 { access, refresh, email }
    Failure  → 401 { error: "<user-facing message>" }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)       # global handler formats this
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    GET /api/auth/profile/
    Returns the authenticated user's profile.
    Success  → 200 { id, username, email, first_name, last_name }
    Failure  → 401 { error: "..." }    (via global handler)
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


class UserIdentifyView(APIView):
    """
    GET /api/auth/user/
    Returns extended info for the authenticated user (used by frontend on init).
    Success  → 200 { id, email, first_name, last_name, is_active, date_joined }
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
        })


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Body: { refresh: "<refresh_token>" }
    Blacklists the refresh token and invalidates the session.
    Success  → 200 { message: "Signed out successfully." }
    Failure  → 400 { error: "..." }
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required to sign out.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            # Token is already invalid or expired — still counts as logged out
            pass

        return Response({'message': 'Signed out successfully.'}, status=status.HTTP_200_OK)
