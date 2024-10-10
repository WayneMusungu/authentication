from django.urls import path
from authentication.views import ForgotPasswordAPIView, LoginView, LogoutView, UpdateUserAPIView, UserProfile, UserRegistration, PasswordResetView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistration.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='registration'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('update-profile/', UpdateUserAPIView.as_view(), name='update-profile'), 
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'), 
    path('logout/', LogoutView.as_view(), name='logout'),
]