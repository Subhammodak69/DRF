from django.urls import path
from .views import RegisterView, LoginView, ProfileView, LogoutView, UserIdentifyView
from rest_framework_simplejwt.views import TokenRefreshView,TokenBlacklistView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user/', UserIdentifyView.as_view(), name='check_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('blacklist/', TokenBlacklistView.as_view(), name='token_blacklist')
]
