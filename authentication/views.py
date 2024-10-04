from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from authentication.models import User
from authentication.serializers import ForgotPasswordSerializer, LoginSerializer, PasswordResetSerializer, UserProfileSerializer, UserSerializer
from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle


class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    throttle_scope = 'login'  # Define the throttle scope for login
    throttle_classes = [ScopedRateThrottle]  # Apply scoped throttling to login
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                
                user = authenticate(email=email, password=password)
                
                if user is not None:
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {'status': True,
                         'refresh': str(refresh),
                         'access': str(refresh.access_token),                        
                        }, status=status.HTTP_200_OK)
                    
                else:
                    return Response(
                        {'detail': 'Authentication failed', 'status': False},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
        except Exception as e:
            return Response(
                {'detail': 'An error occurred: ' + str(e), 'status': False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

            
class UserProfile(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user


class PasswordResetView(generics.UpdateAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            
            user.set_password(new_password)
            user.save()
            
            return Response({
                "detail": "Password has been reset successfully."
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ForgotPasswordAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            return Response({
                "detail": "Password has been reset successfully."
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        