from rest_framework import serializers
from authentication.models import User
import re
from django.core.exceptions import ValidationError

def validate_special_character(value):
    # This is a custom validator that adds aditional layer of complexity to ensure passwords
    # includes characters beyond alpha numeric ones
    pattern = r'[\W_]+'
    if not re.search(pattern, value):
        raise ValidationError('Password must contain at least one special character eg."~!@#$%^&*"')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_special_character])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Password do not match"})
        
        return data

    def create(self, validated_data):
        # Remove confirm_password before creating the user
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(**validated_data)
        return user
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)