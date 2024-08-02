from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from authentication.models import User
from authentication.serializers import LoginSerializer, UserSerializer


class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
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

        
        