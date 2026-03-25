"""
user/urls.py
============
URL configuration for the ``user`` authentication app.

All routes are mounted under ``/api/auth/`` by the project-level urls.py.

Route Map
---------
+----------------------------------+-------------------------------------+
| URL Pattern                      | View                                |
+==================================+=====================================+
| POST  register/                  | RegisterView                        |
| POST  login/                     | LoginView                           |
| POST  logout/                    | LogoutView                          |
| GET   profile/                   | ProfileView                         |
| GET   user/                      | UserIdentifyView                    |
| POST  token/refresh/             | TokenRefreshView (SimpleJWT)        |
| POST  blacklist/                 | TokenBlacklistView (SimpleJWT)      |
+----------------------------------+-------------------------------------+
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from user.views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    UserIdentifyView,
)

urlpatterns = [
    # ── Authentication ───────────────────────────────────────────────────────
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/",    LoginView.as_view(),    name="auth-login"),
    path("logout/",   LogoutView.as_view(),   name="auth-logout"),

    # ── Profile / Identity ───────────────────────────────────────────────────
    path("profile/", ProfileView.as_view(),       name="auth-profile"),
    path("user/",    UserIdentifyView.as_view(),   name="auth-user-identify"),

    # ── Token Management (SimpleJWT built-in) ───────────────────────────────
    path("token/refresh/", TokenRefreshView.as_view(),   name="token-refresh"),
    path("blacklist/",     TokenBlacklistView.as_view(), name="token-blacklist"),
]
