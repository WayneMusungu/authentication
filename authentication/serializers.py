from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User
import re
from django.core.exceptions import ValidationError
from authentication.validators import allow_only_images_valdators

def validate_special_character(value):
    # This is a custom validator that adds aditional layer of complexity to ensure passwords
    # includes characters beyond alpha numeric ones
    pattern = r'[\W_]+'
    if not re.search(pattern, value):
        raise ValidationError('Password must contain at least one special character eg."~!@#$%^&*"')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_special_character])
    confirm_password = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=True, allow_null=False, validators=[allow_only_images_valdators])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'profile_picture')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password do not match"})
        return data

    def create(self, validated_data):
        # Remove confirm_password before creating the user
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(**validated_data)
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'profile_picture', 'created_date')

    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def authenticate_user(self):
        email = self.validated_data['email']
        password = self.validated_data['password']
        
        user = authenticate(email=email, password=password)
        
        if user is None:
            return None, None
        
        refresh = RefreshToken.for_user(user)
        tokens = {
            'status': True,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return user, tokens
         

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_special_character])
    confirm_password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password do not match"})
        return data
    

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True, validators=[validate_special_character])
    confirm_password = serializers.CharField(write_only=True)
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"email": "User with this email does not exist"})
        return value
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password do not match"})
        return data