from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import User, Referral


class ConfirmEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['token', 'uidb64']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer): 

    """Override default token login to include user data"""

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not user.is_verified:
            raise serializers.ValidationError({"error":"Email is not verified."})

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


class ReferralSerializer(serializers.ModelSerializer):
    referrer = UserSerializer()
    referred = UserSerializer()

    class Meta:
        model = Referral
        fields = (
            'id',
            'referrer',
            'referred',
            'date_referred',
        )



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6)
    referral_code = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'password', 
            'role', 
            'referral_code',
                       
        )

        extra_kwargs = {
            "is_active": {"read_only": True},
            "is_verified": {"read_only": True},
            "password": {"write_only": True},
            "user_permissions": {"read_only": True},
        }

    def create(self, validated_data):
        # Get the referral code from the request data
        referral_code = validated_data.pop('referral_code', None)

        # Create the user object
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
        )

        # if referral code is provided, associate the user with the referrer 
        if referral_code:
            try:
                # Get the referrer user object 
                referrer = User.objects.get(referral_code=referral_code)

                # Associate the referred user with the referrer 
                Referral.objects.create(referrer=referrer, referred=user)
            except User.DoesNotExist:
                pass

        return user
        




