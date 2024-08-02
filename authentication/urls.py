from django.urls import path

from authentication.views import LoginView, UserRegistration

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='registration'),
]