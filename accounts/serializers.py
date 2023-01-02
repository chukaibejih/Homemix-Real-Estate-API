from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import User

# User = get_user_model


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer): 

    """Overide default token login to include user data"""

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update(
            {
                "id": self.user.id,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "is_superuser": self.user.is_superuser,
                "is_staff": self.user.is_staff,
                "is_verified": self.user.is_verified
            }
        )

        return data


class UserSerializer(serializers.ModelSerializer):
     class Meta:
            model = User
            fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'premium',
            'role',
            'is_active',
            'is_verified',
            'created_at',
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6)

    class Meta:
        model = User
        fields = (
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'role', 
            'password',            
        )

        extra_kwargs = {
            "is_active": {"read_only": True},
            "is_verified": {"read_only": True},
            "password": {"write_only": True},
            "user_permissions": {"read_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
        validated_data['email'],
        validated_data['password'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        role=validated_data['role'],
    )

        return user




