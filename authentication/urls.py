from django.urls import path

from authentication.views import ForgotPasswordAPIView, LoginView, UserProfile, UserRegistration, PasswordResetView

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='registration'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'), 
]